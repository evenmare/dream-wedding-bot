"""Package contains commands implementatins."""

import inspect
import sys
from typing import Callable

from applications.commands.sync_available_commands import SyncAvailableCommandsCommand  # noqa: F401
from applications.commands.assign_public_notifications import AssignPublicNotificationsCommand  # noqa: F401
from applications.commands.send_notification import SendNotificationCommand  # noqa: F401

COMMANDS_MAPPING: dict[str, Callable] = {
    command_cls.command_name: command_cls
    for _, command_cls in inspect.getmembers(sys.modules[__name__])
    if inspect.isclass(command_cls)
}
