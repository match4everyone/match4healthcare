from django.conf import settings
import sendgrid
import logging

logger = logging.getLogger(__name__)


def send_mass_mail_sendgrid(
    recipient_list, subject, html_body, from_mail=settings.NOREPLY_MAIL, use_sandbox_mode=False,
):
    if len(recipient_list) > 950:
        raise ValueError(
            "Cannot send a mail to more then 1k recipients, see "
            "https://sendgrid.com/docs/API_Reference/Web_API_v3/Mail/index.html#-Limitations."
        )

    if len(recipient_list) == 0:
        # Nothing to send
        return None

    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

    recipients_personalisations = [{"to": [{"email": mail}]} for mail in recipient_list]

    data = {
        "personalizations": recipients_personalisations,
        "subject": subject,
        "content": [{"type": "text/html", "value": html_body}],
        "from": {"email": from_mail},
        "mail_settings": {"sandbox_mode": {"enable": use_sandbox_mode}},
    }

    response = sg.client.mail.send.post(request_body=data)

    # check if errors occured
    if response.status_code != 202:
        logger.error(
            "A newsletter could not be delivered, the sendgrid API did not queue them.",
            extra={
                "status_code": response.status_code,
                "body": response.body,
                "headers": response.headers,
                "newsletter_subject": subject,
                "newsletter_body": html_body,
            },
        )
    else:
        logger.info("Sent out a newsletter to %s recipients." % len(recipient_list))
