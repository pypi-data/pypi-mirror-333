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

__all__ = ["construct_topic", "extract_topic"]


def construct_topic(value: str, class_name: str) -> tuple[str, str]:
    """Constructs a name and qualified topic.

    :param value: The name of the topic.
    :type value: str
    :param class_name: Name of the calling class to raise sensible error.
    :type class_name: str
    """
    if value.endswith("."):
        raise ValueError(f"{class_name} name cannot end with '.'")
    if value.startswith("."):
        value = value[1:]
        topic = value
    else:
        topic = f"-.{value}" if value else "-"
    return value, topic


def extract_topic(value: str) -> str:
    """Extracts topic from qualified topic name.

    This cuts off a possible ``-.`` at the beginning of the topic name.

    :param value: The qualified name of the topic.
    :type value: str
    """
    return value[2:] if value.startswith("-") else value
