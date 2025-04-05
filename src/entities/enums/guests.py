"""Module contains guest Enums."""
import enum


class GuestCategoryEnum(enum.Enum):
    """List of guest categories."""

    RELATIVE = 'relative'
    FRIEND = 'friend'
    WITNESS = 'witness'
