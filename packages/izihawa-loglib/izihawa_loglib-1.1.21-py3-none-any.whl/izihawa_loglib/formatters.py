import dataclasses
import datetime
import logging
import os
import pprint
import time
import traceback
import typing

import orjson as json
from izihawa_utils.exceptions import BaseError

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class BaseFormatter(logging.Formatter):
    def _prepare(self, record):
        if isinstance(record.msg, BaseError):
            return record.msg.as_internal_dict()
        elif isinstance(record.msg, typing.Dict) or dataclasses.is_dataclass(
            record.msg
        ):
            return record.msg
        else:
            return dict(message=super().format(record))

    def format(self, record):
        log_record = self._prepare(record)
        return json.dumps(log_record).decode()


class DefaultHttpFormatter(BaseFormatter):
    def _prepare(self, record):
        log_record = super()._prepare(record)

        timestamp = time.time()
        formatted_datetime = datetime.datetime.fromtimestamp(timestamp).strftime(
            DATETIME_FORMAT
        )
        real_ip = getattr(record, "real_ip", None)
        request_id = getattr(record, "request_id", None)
        client_id = getattr(record, "client_id", None)
        method = getattr(record, "method", None)
        path = getattr(record, "path", None)

        log_record.update(
            unixtime=int(timestamp),
            timestamp=int(timestamp * 1_000_000),
            datetime=formatted_datetime,
            process=os.getpid(),
        )

        if real_ip:
            log_record["real_ip"] = real_ip
        if request_id:
            log_record["request_id"] = request_id
        if client_id:
            log_record["client_id"] = client_id
        if method:
            log_record["method"] = method
        if path:
            log_record["path"] = path

        return log_record

    def format(self, record):
        log_record = self._prepare(record)
        return json.dumps(log_record).decode()


class DefaultFormatter(BaseFormatter):
    def _prepare(self, record):
        log_record = super()._prepare(record)

        timestamp = time.time()
        formatted_datetime = datetime.datetime.fromtimestamp(timestamp).strftime(
            DATETIME_FORMAT
        )
        log_record.update(
            unixtime=int(timestamp),
            timestamp=int(timestamp * 1_000_000),
            datetime=formatted_datetime,
            process=os.getpid(),
        )
        return log_record

    def format(self, record):
        log_record = self._prepare(record)
        return json.dumps(log_record, default=str).decode()


class TracebackFormatter(DefaultFormatter):
    def format(self, record):
        log_record = self._prepare(record)
        if traceback.sys.exc_info()[0] is not None:
            value = pprint.pformat(log_record, indent=2)
            value += "\n" + traceback.format_exc()
        else:
            value = json.dumps(log_record).decode()
        return value


default_formatter = DefaultFormatter()
default_traceback_formatter = TracebackFormatter()
