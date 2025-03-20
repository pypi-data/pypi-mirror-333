#  hakisto - logging reimagined
#
#  Copyright (C) 2024  Bernhard Radermacher
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.


# logger using PyPubSub to improve flexibility

import inspect
import sys
import threading
from types import FrameType, TracebackType

from ._logger_globals import LoggerGlobals
from .pub_sub import send_message
from .severity import TRACE, DEBUG, VERBOSE, INFO, SUCCESS, WARNING, ERROR, CRITICAL
from .subject import Subject
from .topic import construct_topic, extract_topic

__all__ = ["Logger"]


def _send_log(topic, subject: Subject) -> None:
    send_message(topic, subject=subject)


class Logger:
    """Main Logger class. Can be inherited from, but should be sufficient for most situations.

    .. include:: logger_name.txt

    :param name: Logger name.
    """

    _globals = LoggerGlobals()
    __lock = threading.RLock()

    def __init__(self, name: str = "", **kwargs) -> None:
        """
        :param kwargs: catch all
        :type kwargs: dict
        """
        self._lock = threading.RLock()
        self._name, self._topic = construct_topic(name, self.__class__.__name__)
        self._severity = None
        self._enabled = True

    def enable(self, enabled: bool = True) -> None:
        self._enabled = enabled

    def disable(self) -> None:
        self.enable(False)

    @staticmethod
    def register_excluded_source_file(file_name: str) -> None:
        logger_globals.register_excluded_source_file(file_name)

    @property
    def severity(self) -> int:
        return self._globals.severity if self._severity is None else self._severity

    @severity.setter
    def severity(self, severity: int | None) -> None:
        """Set minimum severity level for which the logger is sending messages.

        :param severity: Minimum severity level. Use **named** levels to be compatible. ``None`` will use the **global** severity.
        """
        with self._lock:
            self._severity = severity

    @property
    def name(self) -> str:
        return self._name

    @property
    def topic(self) -> str:
        return self._topic

    def critical(self, *args: str, message_id: str = None, force_location: bool = False, **kwargs) -> None:
        """Log a **CRITICAL** entry.

        ``CRITICAL`` entries will include the respective source location, source section and local variables.

        :param args: The Message(s). Every message will create a separate entry.
        :param message_id: Message ID.
        :param force_location: Force output of location
        """
        self.log(CRITICAL, message_id=message_id, force_location=force_location, *args, **kwargs)

    def error(self, *args: str, message_id: str = None, force_location: bool = False, **kwargs) -> None:
        """Log an **ERROR** entry.

        ``ERROR`` entries will include the respective source location.

        :param args: The Message(s). Every message will create a separate entry.
        :param message_id: Message ID.
        :param force_location: Force output of location
        """
        self.log(ERROR, message_id=message_id, force_location=force_location, *args, **kwargs)

    def warning(self, *args: str, message_id: str = None, force_location: bool = False, **kwargs) -> None:
        """Log a **WARNING** entry.

        :param args: The Message(s). Every message will create a separate entry.
        :param message_id: Message ID.
        :param force_location: Force output of location
        """
        self.log(WARNING, message_id=message_id, force_location=force_location, *args, **kwargs)

    def success(self, *args: str, message_id: str = None, force_location: bool = False, **kwargs) -> None:
        """Log a **SUCCESS** entry.

        This has been added to support responses from SAP.

        :param args: The Message(s). Every message will create a separate entry.
        :param message_id: Message ID.
        :param force_location: Force output of location
        """
        self.log(SUCCESS, message_id=message_id, force_location=force_location, *args, **kwargs)

    def info(self, *args: str, message_id: str = None, force_location: bool = False, **kwargs) -> None:
        """Log an **INFO** entry.

        :param args: The Message(s). Every message will create a separate entry.
        :param message_id: Message ID.
        :param force_location: Force output of location
        """
        self.log(INFO, message_id=message_id, force_location=force_location, *args, **kwargs)

    def verbose(self, *args: str, message_id: str = None, force_location: bool = False, **kwargs) -> None:
        """Log a **VERBOSE** entry.

        :param args: The Message(s). Every message will create a separate entry.
        :param message_id: Message ID.
        :param force_location: Force output of location
        """
        self.log(VERBOSE, message_id=message_id, force_location=force_location, *args, **kwargs)

    def debug(self, *args: str, message_id: str = None, force_location: bool = False, **kwargs) -> None:
        """Log a **DEBUG** entry.

        :param args: The Message(s). Every message will create a separate entry.
        :param message_id: Message ID.
        :param force_location: Force output of location
        """
        self.log(DEBUG, message_id=message_id, force_location=force_location, *args, **kwargs)

    def trace(self, *args: str, message_id: str = None, force_location: bool = False, **kwargs) -> None:
        """Log a **TRACE** entry.

        :param args: The Message(s). Every message will create a separate entry.
        :param message_id: Message ID.
        :param force_location: Force output of location
        """
        self.log(TRACE, message_id=message_id, force_location=force_location, *args, **kwargs)

    def log(self, severity, *args: str, message_id: str = None, force_location: bool = False, **kwargs) -> None:
        """Log an entry.

        While this method has been made public, be advised, that using integers directly might break in the
        future, if the implementation is modified.

        :param severity: The severity level of the log entry.
        :param args: The Message(s). Every message will create a separate entry.
        :param message_id: Message ID.
        :param force_location: Force output of location
        """
        if not self._enabled or severity < self.severity:
            return
        frame = self._get_caller()
        for message in args:
            self._send_log(
                Subject(
                    topic=extract_topic(self.topic),
                    severity=severity,
                    frame=frame,
                    message=str(message),
                    message_id=message_id,
                    force_location=force_location,
                    **kwargs,
                )
            )

    def set_handler_severity(self, severity: int) -> None:
        """Set the minimum severity for all Handlers listening to the logger's topic.

        :param severity: New severity.
        """
        # noinspection PyTypeChecker
        self._send_log(
            Subject(
                topic=extract_topic(self.topic),
                severity=severity,
                frame=None,
                message=None,
                message_id=None,
                __set_severity__=severity,
            )
        )

    def set_date_format(self, date_format: str) -> None:
        """Set the date format for all Handlers listening to the logger's topic.

        :param date_format: New date format.
        """
        # noinspection PyTypeChecker
        self._send_log(
            Subject(
                topic=extract_topic(self.topic),
                severity=0,
                frame=None,
                message=None,
                message_id=None,
                __set_date_format__=date_format,
            )
        )

    def _get_caller(self) -> FrameType:
        """Return *real* caller.

        If this method is overridden, make sure that the right frames are excluded.

        :meta public:
        """
        frame = inspect.currentframe()
        while frame.f_code.co_filename in self._globals.excluded_source_files:
            frame = frame.f_back
        return frame

    def _send_log(self, subject: Subject) -> None:
        _send_log(self.topic, subject=subject)

    def __repr__(self):
        return f"Logger(name='{self.name}')"


def log_exception(exception_class, exception: Exception, trace_back: TracebackType):
    """Hook to handle uncaught exceptions.

    The entry is sent to **all** Handlers.

    A :class:`imuthes.logging.Handler` **must** implement ``handle_exception`` when it should react to this.

    :param exception_class: Not used
    :type exception_class: object
    :param exception:
    :param trace_back:
    """
    _send_log("-", subject=Subject(topic="-", severity=sys.maxsize, frame=trace_back, message=str(exception)))


logger_globals = LoggerGlobals()
logger_globals.register_excluded_source_file(inspect.currentframe().f_code.co_filename)
sys.excepthook = log_exception
