class BaseException(Exception):
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