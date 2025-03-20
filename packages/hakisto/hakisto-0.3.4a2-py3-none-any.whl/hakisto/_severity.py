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
]

# fmt: off
TRACE    = 100  # More information than regular DEBUG (e.g. variable values).
DEBUG    = 200  # Debugging (technical) information.
VERBOSE  = 300  # Additional (non-technical) information.
INFO     = 400  # Information.
SUCCESS  = 500  # Successful execution.
WARNING  = 600  # Warning that might require attention.
ERROR    = 800  # Significant issue. Processing might continue.
CRITICAL = 900  # Critical issue. Usually processing is aborted.

severities = MappingProxyType({
    TRACE:    'TRACE',
    DEBUG:    'DEBUG',
    VERBOSE:  'VERBOSE',
    INFO:     'INFO',
    SUCCESS:  'SUCCESS',
    WARNING:  'WARNING',
    ERROR:    'ERROR',
    CRITICAL: 'CRITICAL',
})
"""Lookup severity name using integer value."""

severity_names = MappingProxyType({
    v: k for k, v in severities.items()
})
"""Lookup severity using name."""
# fmt: on
