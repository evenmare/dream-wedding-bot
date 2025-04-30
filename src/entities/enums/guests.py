"""Module contains guest Enums."""

import enum


class GuestGenderEnum(str, enum.Enum):
    """List of guest genders."""

    FEMALE = 'F'
    MALE = 'M'


class GuestCategoryEnum(str, enum.Enum):
    """List of guest categories."""

    RELATIVE = 'relative'
    FRIEND = 'friend'
    WITNESS = 'witness'
