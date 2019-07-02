import collections
import os
from datetime import datetime

import structlog
from structlog import (
        PrintLogger,
        wrap_logger,
)
from structlog.processors import (
        JSONRenderer,
)


USE_STDLIB = bool(os.getenv("ESLOG_USE_STDLIB"))


def order_fields(_, level, event_dict):

    response = collections.OrderedDict()
    response['level'] = level
    response['message'] = event_dict.pop('event')
    response['timestamp'] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    response.update(sorted(event_dict.items()))
    return response


if USE_STDLIB:
    structlog.configure(
        processors=[
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )


class Logger():

    def __init__(self, output=None, service=None, namespace=None):

        if USE_STDLIB:
            log = structlog.getLogger(
               processors=[
                   structlog.stdlib.filter_by_level,
                   structlog.stdlib.add_logger_name,
                   structlog.stdlib.add_log_level,
                   structlog.stdlib.PositionalArgumentsFormatter(),
                   structlog.processors.StackInfoRenderer(),
                   structlog.processors.format_exc_info,
                   structlog.processors.UnicodeDecoder(),
                   structlog.stdlib.render_to_log_kwargs,
               ],
               context_class=dict,
               wrapper_class=structlog.stdlib.BoundLogger,
            )
        else:
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
        self._logger.debug(msg, **dict(kwargs))

    def info(self, msg, **kwargs):
        self._logger.info(msg, **dict(kwargs))

    def warn(self, msg, **kwargs):
        self._logger.warn(msg, **dict(kwargs))

    def error(self, msg, **kwargs):
        self._logger.error(msg, **dict(kwargs))
