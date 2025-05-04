"""Module contains exceptions for repositories implementations."""


class BaseRepositoryException(Exception):
    """Base repository exception."""

    code: str = ''
    details: str

    def __init__(self, details: str, *args):
        """Class constructor."""
        self.details = details
        super().__init__(details, *args)

    def __repr__(self) -> str:
        """Exception representation."""
        return f'{self.code}: {self.details}'


class ObjectNotFoundException(BaseRepositoryException):
    """Not found in repository exception."""

    code: str = 'Object Not Found'


class IntegrityError(BaseRepositoryException):
    """Integrity error."""

    code: str = 'Integrity Error'
