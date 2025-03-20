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

#  Handlers (listeners) are attached using pypubsub, but we want to isolate this
#  from other usages.

from types import MappingProxyType

from ._colors import RED, GREEN, YELLOW, MAGENTA, CYAN, LIGHT_RED, LIGHT_GREEN, LIGHT_YELLOW, LIGHT_MAGENTA, LIGHT_CYAN
from ._severity import TRACE, DEBUG, VERBOSE, INFO, SUCCESS, WARNING, ERROR, CRITICAL, severities, severity_names

__all__ = [
    "TRACE",
    "DEBUG",
    "VERBOSE",
    "INFO",
    "SUCCESS",
    "WARNING",
    "ERROR",
    "CRITICAL",
    "severities",
    "severity_names",
    "severity_colors",
    "light_severity_colors",
    "dark_severity_colors",
]

severity_colors = MappingProxyType(
    {
        TRACE: LIGHT_MAGENTA,
        DEBUG: LIGHT_CYAN,
        VERBOSE: LIGHT_GREEN,
        INFO: LIGHT_GREEN,
        SUCCESS: LIGHT_GREEN,
        WARNING: LIGHT_YELLOW,
        ERROR: LIGHT_RED,
        CRITICAL: LIGHT_RED,
    }
)
"""Default colors for severities."""

light_severity_colors = severity_colors
"""Default light colors for severities."""

dark_severity_colors = MappingProxyType(
    {
        TRACE: MAGENTA,
        DEBUG: CYAN,
        VERBOSE: GREEN,
        INFO: GREEN,
        SUCCESS: GREEN,
        WARNING: YELLOW,
        ERROR: RED,
        CRITICAL: RED,
    }
)
"""Default dark colors for severities."""
# fmt: on
