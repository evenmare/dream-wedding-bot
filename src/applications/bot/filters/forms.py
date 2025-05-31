"""Module implements logic for Guest form filters."""

from typing import Sequence

from dependency_injector.wiring import inject, Provide
from telebot.types import Message, CallbackQuery
from telebot.asyncio_filters import AdvancedCustomFilter

from containers import Container
from applications.bot.context import request_guest, request_guest_form
from entities.enums.forms import GuestFormStageEnum
from entities.schemas.forms import GuestFormSchema
from entities.schemas.guests import GuestSchema
from exceptions.repositories import ObjectNotFoundException
from repositories.database.forms import GuestFormRepository


class FormStageFilter(AdvancedCustomFilter):
    """Class implements filter on guest form stage."""

    key = 'form_stage'

    @inject
    async def check(
        self,
        _: Message | CallbackQuery,
        text: Sequence[GuestFormStageEnum],
        repository: GuestFormRepository = Provide[Container.guest_form_repository],
    ) -> bool:
        """Validates if guest form stage contained in sequence.

        :param message: Telebot Message object.
        :param text: Sequence of expected stages.
        :return: Guest form stage is a value of sequence?
        """
        guest: GuestSchema = request_guest.get()

        try:
            guest_form: GuestFormSchema = await repository.get_by_guest_id(guest_id=guest.guest_id)
        except ObjectNotFoundException:
            return False

        request_guest_form.set(guest_form)

        return guest_form.stage in text
