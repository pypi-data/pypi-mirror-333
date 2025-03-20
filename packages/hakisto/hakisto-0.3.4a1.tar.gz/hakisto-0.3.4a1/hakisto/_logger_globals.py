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

import os
import threading
from ._severity import severity_names


class LoggerGlobals:
    """Singleton to store global information for logging"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LoggerGlobals, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._severity = severity_names.get(os.getenv("HAKISTO_SEVERITY", "").upper(), 0)
        self._output_to_file = False
        self._use_color = True
        self._short_trace = False
        self._inline_location = set()
        self._excluded_source_files = set()

    def register_excluded_source_file(self, file_name: str) -> None:
        """This must be called in the source file of any descendent to exclude the respective
        entries in the call-stack.

        Recommendation: Call on source file level (module).

        .. code:: python

           Logger.register_excluded_source_file(inspect.currentframe().f_code.co_filename)

        :param file_name: Source file name
        """
        with self._lock:
            self._excluded_source_files.add(file_name)

    @property
    def excluded_source_files(self) -> set[str]:
        """Get a copy of excluded_source_files when identifying *real* caller in call-stack."""
        return self._excluded_source_files.copy()

    @property
    def severity(self) -> int:
        return self._severity

    @severity.setter
    def severity(self, value: int | str):
        if isinstance(value, str):
            value = severity_names.get(value.upper(), 0)
        with self._lock:
            self._severity = value

    @property
    def output_to_file(self) -> bool:
        return self._output_to_file

    @output_to_file.setter
    def output_to_file(self, value: bool):
        with self._lock:
            self._output_to_file = value

    @property
    def use_color(self) -> bool:
        return self._use_color

    @use_color.setter
    def use_color(self, value: bool):
        with self._lock:
            self._use_color = value

    @property
    def short_trace(self) -> bool:
        return self._short_trace

    @short_trace.setter
    def short_trace(self, value: bool):
        with self._lock:
            self._short_trace = value

    @property
    def inline_location(self) -> set:
        return self._inline_location


logger_globals = LoggerGlobals()
