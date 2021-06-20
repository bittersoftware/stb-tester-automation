# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""

    pass


class NotInScreen(Error):
    """Raised when not in the expected page object"""

    pass


class NotFound(Error):
    """Raised when the input you are looking for is not found"""

    pass


class ArgumentNotValid(Error):
    """Raised when the argument is not valid"""

    pass


class TimeoutError(Error):
    """Raised when the element not found in time"""

    pass
