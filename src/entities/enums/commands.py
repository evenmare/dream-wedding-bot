"""Module conatins enums of bot commands."""

from enum import Enum


class CommandEnum(str, Enum):
    """Enum contains available bot commands."""

    START = 'start'
    CEREMONY_INFO = 'ceremony_info'
    REGISTRATION_INFO = 'registration_info'
