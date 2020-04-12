from enum import Enum
from datetime import datetime
import json_log_formatter
import logging

class LogLevel(Enum):
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warn'
    ERROR = 'error'
    CRITICAL = 'error'


class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        """
        Format an exception so that it prints on a single line.
        """
        result = super(OneLineExceptionFormatter, self).formatException(exc_info)
        return repr(result)  # or format into one line however you want to

    def format(self, record):
        s = super(OneLineExceptionFormatter, self).format(record)
        if record.exc_text:
            s = s.replace('\n', '') + '|'
        return s

class DjangoRequestJSONFormatter(json_log_formatter.JSONFormatter):
    def json_record(self, message, extra, record):

        extra['level'] = LogLevel[record.levelname].value
        extra['message'] = '[{}]: {}'.format(record.name, record.getMessage())
        if 'timestamp' not in extra:
            extra['timestamp'] = datetime.utcnow()
        if hasattr(record,'request'):
            # Overwrite request information in extra, avoid circular references by copying only selected items
            extra['request'] = {} 
            if hasattr(record.request,'user'):
                extra['user'] = str(record.request.user)
            
            request_attributes = ['method','GET','POST','path',]
            for attr in request_attributes:
                extra['request'][attr] = getattr(record.request,attr,'N/A')

        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)


        return extra