class Unauthorized(Exception):
    """
    The Authorization header was validated but the requestor does not have
    the correct permissions to access the requested resource or perform
    the requested operation.
    """


class ApiError(Exception):
    """
    Unexpected error returned by the supplier API.
    """


class InvalidRequest(Exception):
    """
    Invalid request (e.g. missing required parameters).
    """
