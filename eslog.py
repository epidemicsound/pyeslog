import collections
import os
from datetime import datetime

from structlog import (
        PrintLogger,
        wrap_logger,
)
from structlog.processors import (
        JSONRenderer,
)


def order_fields(_, level, event_dict):

    response = collections.OrderedDict()
    response['level'] = level
    response['message'] = event_dict.pop('message')
    response['timestamp'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    response.update(sorted(event_dict.items()))
    return response


class Logger():

    def __init__(self, output=None, service=None, namespace=None):

        log = wrap_logger(
                PrintLogger(output),
                processors=[
                    order_fields,
                    JSONRenderer(),
                ])

        if service is None:
            self._service = os.getenv('SERVICE_NAME', '')
        else:
            self._service = service

        self._logger = log.bind(service=self._service)

        if namespace is not None:
            self._logger = self._logger.bind(namespace=namespace)

    def debug(self, msg, **kwargs):
        self._logger.debug(**dict(kwargs, message=msg))

    def info(self, msg, **kwargs):
        self._logger.info(**dict(kwargs, message=msg))

    def warn(self, msg, **kwargs):
        self._logger.warn(**dict(kwargs, message=msg))

    def error(self, msg, **kwargs):
        self._logger.error(**dict(kwargs, message=msg))
