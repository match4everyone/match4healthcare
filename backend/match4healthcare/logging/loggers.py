import requests
import json
import logging
from _collections import defaultdict

logger = logging.getLogger(__name__)

emoji = defaultdict(lambda: ":clown_face:")
emoji["WARNING"] = ":thinking_face:"
emoji["ERROR"] = ":face_with_thermometer:"
emoji["INFO"] = ":male-teacher:"
emoji["CRITICAL"] = ":bomb:"
emoji["DEBUG"] = ":female-mechanic:"


def SlackMessageHandlerFactory(webhook_url):
    return SlackMessageHandler(webhook_url)


class SlackMessageHandler(logging.Handler):
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        super().__init__()

    def create_block(self, name, value):
        return {"type": "mrkdwn", "text": "*{}*:\n{}".format(name, value)}

    # replacing default django emit (https://github.com/django/django/blob/master/django/utils/log.py)
    def emit(self, record: logging.LogRecord, *args, **kwargs):

        # Check if a logging url was set
        if self.webhook_url == None or self.webhook_url == "":
            return

        if getattr(record, "logHandlerException", None) == self.__class__:
            return  # This error was caused in this handler, no sense in trying again

        req = getattr(record, "request", None)
        request_fields = []
        request_fields.append(
            self.create_block("Method", getattr(req, "method", "n/a"))
        )
        request_fields.append(self.create_block("Path", getattr(req, "path", "n/a")))
        request_fields.append(
            self.create_block("Status Code", getattr(record, "status_code", "n/a"))
        )

        message = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "{} *{}*:\n[{}]: {}".format(
                            emoji[record.levelname],
                            record.levelname,
                            record.name,
                            record.getMessage(),
                        ),
                    },
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": "*Level*:\n{}".format(record.levelname),
                        },
                        *request_fields,
                    ],
                },
            ]
        }

        try:
            requests.post(self.webhook_url, data=json.dumps(message))
        except requests.exceptions.RequestException as e:  # Catch all request related exceptions
            logger.exception(
                "Exception while trying to send a log message to Slack",
                exc_info=e,
                extra={"logHandlerException": self.__class__},
            )
