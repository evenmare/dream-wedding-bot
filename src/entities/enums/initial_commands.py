"""Module contains Initial commands enums."""

import enum


class InitialCommandEnum(str, enum.Enum):
    """Initial command list."""

    REQUEST_CONTACT = 'request_contact'
    REGISTRATION_FAILED = 'registration_failed'
