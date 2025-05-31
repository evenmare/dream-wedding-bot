"""Module contains typings for services implementations."""

import re
from typing import TYPE_CHECKING, NamedTuple

from entities.enums.entities import ContextEntityEnum

if TYPE_CHECKING:
    from entities.schemas.callbacks import MessageReferenceSchema

LANGUAGE_RFC2616_REGEXP = r'^(?:[A-Za-z]{1,8}(?:-[A-Za-z]{1,8})*|\*)$'
LANGUAGE_RFC2616_PATTERN = re.compile(LANGUAGE_RFC2616_REGEXP)

RequiredMessageContextDict = dict[ContextEntityEnum, list[str]]


class CoordinatesTuple(NamedTuple):
    """Tuple of coordinates."""

    latitude: float
    longitude: float


class MessageFactoryDataTuple[CommandSchemaType](NamedTuple):
    """Tuple of message factory data."""

    message_ref: 'MessageReferenceSchema'
    commands: 'list[CommandSchemaType] | None'
