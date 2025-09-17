"""Module contains guest Enums."""

from enum import Enum


class GuestGenderEnum(str, Enum):
    """List of guest genders."""

    FEMALE = 'F'
    MALE = 'M'


class GuestCategoryEnum(str, Enum):
    """List of guest categories."""

    NEWLYWEDS = 'newlyweds'
    RELATIVE = 'relative'
    FRIEND = 'friend'
    WITNESS = 'witness'
