class ProteusException(Exception):
    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.__doc__)


class UserAlreadyExists(ProteusException):
    """Username/email is already taken"""
