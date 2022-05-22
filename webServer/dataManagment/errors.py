
class DataError(Exception):
    """Base class for exceptions in this module."""
    pass

class AuthTokenError(DataError):
    """Exception raised for errors in the AuthToken.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        
class DataNotFoundError(DataError):
    """Exception raised for errors in the Data.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message