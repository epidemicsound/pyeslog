import collections
import os
from datetime import datetime
import logging
from structlog import wrap_logger
from structlog.processors import (
        JSONRenderer,
)


def order_fields(_logger, _method_name, event_dict):

    response = collections.OrderedDict()
    response['message'] = event_dict.pop('message')

    response.update(sorted(event_dict.items()))
    return response


def add_timestamp(_logger, _method_name, event_dict):
    event_dict['timestamp'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    return event_dict


def add_level(_, method_name, event_dict):
    event_dict['level'] = method_name
    return event_dict


class Logger():

    def __init__(self, output=None, service=None, namespace=None):

        log = wrap_logger(
                logging.getLogger(__name__),
                processors=[
                    add_level,
                    add_timestamp,
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
