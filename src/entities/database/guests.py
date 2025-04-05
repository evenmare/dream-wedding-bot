"""Module contains implementations of guest models."""
from tortoise import fields
from tortoise.validators import MinLengthValidator

from entities.database.base import BaseOrmModel
from entities.enums.guests import GuestCategoryEnum


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
    )
    birth_date = fields.DateField()

    class Meta:
        table = 'guests'


class GuestInfo(BaseOrmModel):
    """Guest info model."""

    category = fields.CharEnumField(GuestCategoryEnum)

    is_resident = fields.BooleanField(default=True)
    is_transportation_needed = fields.BooleanField(default=False)
    is_registration_guest = fields.BooleanField(default=False)

    guest = fields.OneToOneField(
        model_name='dream_wedding_bot.Guest',
        related_name='info',
    )

    class Meta:
        table = 'guests_info'
