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

from abc import ABCMeta, abstractmethod
from collections import defaultdict
from typing import NamedTuple

from ._logger_globals import LoggerGlobals
from .colors import colorize_string
from .pub_sub import subscribe
from .subject import FrameInformation
from .topic import construct_topic
from ._severity import CRITICAL, severities, ERROR

# from ._logger import Logger

__all__ = ["Identifier", "Handler"]

logger_globals = LoggerGlobals()


class Identifier(NamedTuple):
    identifier: str
    """.. include:: identifier.txt"""
    continuation: str
    """Only the indicator, indented for use in additional lines."""


class Handler(metaclass=ABCMeta):
    """Ancestor of every concrete Handler.

    A handler processes a possible log entry and adds it to the respective log.

    .. warning:: This class **must** be the last in the list of inherited classes to allow correct processing via Mixin classes.

    .. include:: handler_name.txt

    :param name: Handler name
    :type name: str, optional
    """

    severity: int = 0
    """The minimum severity that the Handler will process."""
    date_format: str = "%y-%m-%d %H:%M:%S"
    """Date format used for default Identifier, UTC is used."""
    colors = defaultdict(lambda: "")

    def __init__(self, name: str = "", **kwargs):
        self.name, self.topic = construct_topic(name, self.__class__.__name__)
        subscribe(self, self.topic)

    def __call__(self, subject):
        """Called when a log entry is processed.

        If message is ``None`` this is a configuration message the respective information should available as directory items.
        """
        if subject.message is None and subject.message_id is None:
            # this is a config message to set the severity or something else
            self.config(subject=subject)
        elif subject.traceback:
            self.handle_exception(subject=subject)
        elif subject.severity >= self.severity:
            self.process(subject=subject)

    # stubs that MUST be implemented by concrete classes

    @abstractmethod
    def render(self, identifier: Identifier, content: str, color: str = "") -> str:
        """Render the provided content for output.

        :param identifier: The identifier that will be used.
        :type identifier: :class:`Identifier`
        :param content: The content to be rendered. Might contain new-line(s).
        :type content: str
        :param color: The color of the content if applicable.
        :type content: str
        :return: The rendered content.
        :rtype: str
        """
        raise NotImplementedError()

    @abstractmethod
    def write(self, content: str):
        raise NotImplementedError()

    # stubs that MIGHT be implemented by concrete classes

    def config(self, subject):
        """Process configuration changes."""
        if "__set_severity__" in subject:
            self.severity = subject["__set_severity__"]
        if "__set_date_format__" in subject:
            self.date_format = subject["__set_date_format__"]

    def process(self, subject):
        color = self.colors[subject.severity]
        content_lines = [colorize_string(subject.message, color)] if subject.severity >= CRITICAL else [subject.message]
        if subject.severity in (ERROR, CRITICAL) or subject.force_location:
            content_lines.append(subject.source_location)
        if subject.severity >= CRITICAL:
            content_lines.append(
                self.format_frame_information(FrameInformation(subject.source.copy(), subject.local_vars.copy()))
            )

        content = self.render(
            identifier=self.get_identifier(subject=subject), content="\n".join(content_lines), color=color
        )
        self.write(content)

    # noinspection PyMethodMayBeStatic
    def format_frame_information(self, frame_information: FrameInformation) -> str:
        """Render Source and local variables for CRITICAL and Exceptions.

        :param frame_information:
        :type frame_information: :class:`hakisto.FrameInformation`
        """
        if not any([frame_information.source, frame_information.local_vars]):
            return ""

        # noinspection PyTypeChecker
        lines: list[tuple[int | str], str] = frame_information.source.copy()
        num_width = len(str(lines[-1][0]))
        txt_width = max((len(i[1]) for i in lines))

        try:
            var_width = max((len(i) for i in frame_information.local_vars))
        except ValueError:
            var_width = 1
        var_lines = [f"   {k:{var_width}} = {v!r}" for k, v in frame_information.local_vars.items()]

        while len(lines) < len(var_lines):
            lines.insert(0, ("", ""))
        while len(lines) > len(var_lines):
            var_lines.insert(0, "")

        return "\n".join(
            [" " * num_width + " ┌──" + "─" * txt_width + "┐"]
            + [f"{lines[i][0]:{num_width}} │ {lines[i][1]:{txt_width}} │{var_lines[i]}" for i in range(len(lines))]
            + [" " * num_width + " └──" + "─" * txt_width + "┘"]
        )

    def handle_exception(self, subject) -> None:
        """Renders the full traceback with source and local variables.

        :param subject: The subject being processed.
        :type subject: :class:`hakisto.Subject`
        """
        color = self.colors[CRITICAL]

        content_lines = [colorize_string(subject.message, color)]
        traceback_blocks = []
        for i in subject.traceback:
            traceback_blocks.append([i.source_location, self.format_frame_information(i.frame_information)])

        if subject.short_trace:
            content_lines.extend(traceback_blocks[-1])
        else:
            for i in traceback_blocks:
                content_lines.extend(i)

        content_lines.append(colorize_string(subject.message, color))

        content = self.render(
            identifier=self.get_identifier(subject=subject, indicator="X"),
            content="\n".join(content_lines),
            color=color,
        )
        self.write(content)

    def get_identifier(self, subject, indicator=None):
        """Return standard Identifier

        .. include:: identifier.txt

        :param subject: The subject to be handled
        :type subject: hakisto.Subject:class:`hakisto.Subject`
        :param indicator: Indicator to use instead of the one determined by Subject.severity
        :type indicator: str
        :returns: Identifier
        :rtype: :class:`hakisto.Identifier`
        """
        indicator = indicator or severities.get(subject.severity, str(subject.severity))[0]
        parts = [f"{indicator} {subject.created.strftime(self.date_format)}"]
        if subject.message_id:
            parts.append(f"<{subject.message_id}>")
        if subject.process_name != "MainProcess":
            parts.append(
                f"*{subject.process_name}:{subject.process_id}*" if subject.process_id else f"*{subject.process_name}*"
            )
        if subject.thread_name != "MainThread":
            parts.append(
                f"({subject.thread_name}:{subject.thread_id})" if subject.thread_id else f"({subject.thread_name})"
            )
        if subject.asyncio_task_name:
            parts.append(f"'{subject.asyncio_task_name}'")
        if subject.severity in logger_globals.inline_location:
            parts.append(f"»{subject.inline_location}«")
        if subject.topic:
            parts.append(subject.topic)
        identifier = f"[{' '.join(parts)}]"
        return Identifier(identifier, f"{' ' * (len(identifier) - len(indicator) - 2)}[{indicator}]")
