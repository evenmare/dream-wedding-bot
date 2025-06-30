"""Module contains context vars implementations."""

from contextvars import ContextVar

from entities.schemas.forms import GuestFormSchema
from entities.schemas.guests import GuestSchema

request_guest: ContextVar[GuestSchema] = ContextVar('request_guest')
request_guest_form: ContextVar[GuestFormSchema] = ContextVar('request_guest_form')
