class PlytixPimClientException(Exception):
    """Base class for exceptions in this module."""


class TokenExpiredError(PlytixPimClientException):
    """Raised when the token has expired"""


class RateLimitExceededError(PlytixPimClientException):
    """Raised when the rate limit has been exceeded"""


class UnprocessableEntityError(PlytixPimClientException):
    """Raised when the request is unprocessable"""


class BadRequestError(PlytixPimClientException):
    """Raised when the request is bad"""


class ConflictError(PlytixPimClientException):
    """Raised when the request is conflicted"""
