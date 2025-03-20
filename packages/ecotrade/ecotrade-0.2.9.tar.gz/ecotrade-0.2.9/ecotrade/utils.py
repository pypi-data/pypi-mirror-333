from functools import wraps
from ecotrade.authentication import Auth

def requires_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not Auth._authenticated:
            raise PermissionError("Auth is required before using this function.")
        return func(*args, **kwargs)
    return wrapper
