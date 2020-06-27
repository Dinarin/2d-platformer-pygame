import functools
def type_check(types, lengths=None, ranges=None):
    """Decorator function that checks type.

    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            for a, t in zip(args, types):
                if not isinstance(a, t):
                    raise TypeError("Expected {}, got {}".format(t, a))
            for a, r in zip(args, lengths):
                if r and not r[0]

            return f(*args, **kwargs)
        return wrapper
    return decorator
