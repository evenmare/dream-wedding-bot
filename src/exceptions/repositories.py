"""Module contains exceptions for repositories implementations."""

from exceptions.base import BaseException


class ObjectNotFoundException(BaseException):
    """Not found in repository exception."""

    code: str = 'Object Not Found'


class IntegrityError(BaseException):
    """Integrity error."""

    code: str = 'Integrity Error'
