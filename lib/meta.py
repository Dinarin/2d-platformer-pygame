import functools
def types_check(types, lengths=None, ranges=None):
    """Decorator function that checks type.
        Args:
            types (list or type): list of types of the arguments.
            lengths (list or int): list of integer lengths
                    of the arguments.
            ranges (list): list of tuples of length 2
                    (min, max) or one tuple.
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            for a, t in zip(args, types):
                if not isinstance(a, t):
                    raise TypeError("Expected {}, got {}".format(t, a))
            for a, l in zip(args, lengths):
                if l and len(a) == l:
                    raise ValueError("Should be of length {}: {}".format(l, a))
            for a, r in zip(args, ranges):
                if r and not r[0] <= a <= r[1]:
                    raise ValueError("Should be of length {}: {}".format(l, a))
            return f(*args, **kwargs)
        return wrapper
    return decorator

def type_check(type, length=None, range=None):
    """Decorator function that checks type.
        Args:
            types (list or type): list of types of the arguments.
            lengths (list or int): list of integer lengths
                    of the arguments.
            ranges (list): list of tuples of length 2
                    (min, max) or one tuple.
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            for a, t in zip(args, types):
                if not isinstance(a, t):
                    raise TypeError("Expected {}, got {}".format(t, a))
            for a, l in zip(args, lengths):
                if l and len(a) == l:
                    raise ValueError("Should be of length {}: {}".format(l, a))
            for a, r in zip(args, ranges):
                if r and not r[0] <= a <= r[1]:
                    raise ValueError("Should be of length {}: {}".format(l, a))
            return f(*args, **kwargs)
        return wrapper
    return decorator
