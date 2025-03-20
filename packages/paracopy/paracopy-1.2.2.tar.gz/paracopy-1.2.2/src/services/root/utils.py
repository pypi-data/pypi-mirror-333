"""Utils for scripts.

Copyright (c) 2024 Pierre-Yves Genest.

This file is part of ParaCopy.

ParaCopy is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, version 3 of the
License.

ParaCopy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with ParaCopy. If not, see <https://www.gnu.org/licenses/>.
"""

from model.script import (
    DeviceCopyMessage,
    DeviceOccupiedSpaceMessage,
    ErrorMessage,
    Messages,
    MessageWrapper,
    ProgressMessage,
    SuccessMessage,
)


def exit_with_error(message: ErrorMessage) -> int:
    """Exit program with error.

    Args:
    ----
        message (ErrorMessage): message to display
    Returns
        int: return code

    """
    print(serialize_message(message), flush=True)  # noqa: T201
    return 1


def exit_with_success(message: SuccessMessage) -> int:
    """Exit program with success.

    Args:
    ----
        message (SuccessMessage): message to display
    Returns
        int: return code

    """
    print(serialize_message(message), flush=True)  # noqa: T201
    return 0


def send_progress(value: float) -> None:
    """Send progress.

    Args:
    ----
        value (float): progress value

    """
    print(serialize_message(ProgressMessage(value=value)), flush=True)  # noqa: T201


def send_device_copy_message(message: DeviceCopyMessage) -> None:
    """Send copy message.

    Args:
    ----
        message (DeviceCopyMessage): copy message

    """
    print(serialize_message(message), flush=True)  # noqa: T201


def send_device_occupied_space_message(message: DeviceOccupiedSpaceMessage) -> None:
    """Send occupied space message.

    Args:
    ----
        message (DeviceOccupiedSpaceMessage): occupied space message

    """
    print(serialize_message(message), flush=True)  # noqa: T201


def serialize_message(message: Messages) -> str:
    """Serialize message.

    Args:
    ----
        message (Messages): message

    """
    return MessageWrapper(message=message).model_dump_json()


def parse_message(message: str) -> Messages:
    """Parse message from string.

    Args:
    ----
        message (str): message
    Returns
        Messages: message

    """
    return MessageWrapper.model_validate_json(message).message


def _(text: str) -> str:
    """Return text itself (internationalization placeholder).

    Args:
    ----
        text (str): text
    Returns
        str: no effect

    """
    return text
