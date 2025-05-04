"""Module contains implementations of guest models."""

from tortoise import fields

from entities.database.base import BaseOrmModel
from entities.enums.guests import GuestCategoryEnum, GuestGenderEnum


class Guest(BaseOrmModel):
    """Guest model."""

    guest_id = fields.IntField(
        primary_key=True,
        generated=True,
    )

    first_name = fields.CharField(
        max_length=16,
        null=False,
    )
    last_name = fields.CharField(
        max_length=32,
        null=False,
    )
    patronymic = fields.CharField(
        max_length=32,
        null=True,
    )
    phone_number = fields.CharField(
        max_length=12,
        null=False,
        unique=True,
        db_index=True,
    )
    birth_date = fields.DateField()
    gender = fields.CharEnumField(
        GuestGenderEnum,
        max_length=1,
    )

    category = fields.CharEnumField(
        GuestCategoryEnum,
        null=False,
    )
    is_resident = fields.BooleanField(
        default=True,
        null=False,
    )
    is_registration_guest = fields.BooleanField(
        default=False,
        null=False,
    )

    class Meta:
        table = 'guests'
