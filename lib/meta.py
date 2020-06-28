import functools
def types_check(*types):
    """Decorator function that checks type.
        Args:
            types (list or type): list of types of the arguments.
            ranges (list): list of tuples of length 2
                    (min, max) or one tuple.
    """
    def decorator(f):
        f_n_args = f.__code__.co_argcount
        if len(types) != f_n_args:
            raise Exception("Expected {}, got {}".format(f_n_args,len(types)))
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            for a, t in zip(args, types):
                if not isinstance(a, t):
                    raise TypeError("Expected {}, got {}".format(t, a))
            return f(*args, **kwargs)
        return wrapper
    return decorator

def len_check(*lengths):
    """Decorator function that checks length.
        Args:
            lengths (list or int): list of integer lengths
                    of the arguments.
    """
    def decorator(f)
        f_n_args = f.__code__.co_argcount
        if len(types) != f_n_args:
            raise Exception("Expected {}, got {}".format(f_n_args,len(types)))
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            for a, t in zip(args, types):
                if not isinstance(a, t):
                    raise TypeError("Expected {}, got {}".format(t, a))
            return f(*args, **kwargs)
        return wrapper
    return decorator

            for a, l in zip(args, lengths):
                if l and len(a) == l:
                    raise ValueError("Should be of length {}: {}".format(l, a))
            for a, r in zip(args, ranges):
                if r and not r[0] <= a <= r[1]:
                    raise ValueError("Should be of length {}: {}".format(l, a))

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
