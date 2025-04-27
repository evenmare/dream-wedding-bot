"""Module contains implementations of guest models."""

from tortoise import fields
from tortoise.validators import MinLengthValidator

from entities.database.base import BaseOrmModel
from entities.enums.guests import GuestCategoryEnum, GuestStatusEnum, GuestGenderEnum


class Guest(BaseOrmModel):
    """Guest model."""

    first_name = fields.CharField(
        max_length=16,
        null=False,
        validators=[MinLengthValidator(2)],
    )
    last_name = fields.CharField(
        max_length=32,
        null=False,
        validators=[MinLengthValidator(2)],
    )
    patronymic = fields.CharField(
        max_length=32,
        null=True,
    )
    phone_number = fields.CharField(
        max_length=12,
        null=False,
        validators=[MinLengthValidator(11)],
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

    status = fields.CharEnumField(
        GuestStatusEnum,
        null=True,
        max_length=16,
    )

    class Meta:
        table = 'guests'
