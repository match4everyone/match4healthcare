import requests
import json
import logging

def SlackMessageHandlerFactory( webhook_url ):
  return SlackMessageHandler(webhook_url)

class SlackMessageHandler(logging.Handler):

  def __init__(self, webhook_url):
    self.webhook_url = webhook_url
    super().__init__()

  def create_block(self,name,value):
    return {
      'type': 'mrkdwn',
      'text': '*{}*:\n{}'.format(name,value)
    }

  # replacing default django emit (https://github.com/django/django/blob/master/django/utils/log.py)
  def emit(self, record: logging.LogRecord, *args, **kwargs):

    req = getattr(record,'request',None)
    request_fields = []
    request_fields.append(self.create_block('Method',getattr(req,'method','n/a')))
    request_fields.append(self.create_block('Path',getattr(req,'path','n/a')))
    request_fields.append(self.create_block('Status Code',getattr(record,'status_code','n/a')))

    message = {
      'blocks': [
        {
          'type': 'section',
          'text': {
            'type': 'mrkdwn',
            'text': '*{}*:\n[{}]: {}'.format(record.levelname, record.name, record.getMessage())
          }
        },
        {
          'type': 'section',
          'fields': [
          {
            'type': 'mrkdwn',
            'text': '*Level*:\n{}'.format(record.levelname)
          },
          *request_fields
          ]
        }
      ]
    }



    if not self.webhook_url == None:
      requests.post(self.webhook_url, data=json.dumps(message))