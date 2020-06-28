import functools
def m_types_check(*types):
    """Decorator function that checks type.
        Args:
            types (list or type): list of types of the arguments.
    """
    def decorator(f):
        f_n_args = f.__code__.co_argcount - 1
        if len(types) != f_n_args:
            raise Exception("Expected {}, got {}".format(f_n_args,len(types)))
        @functools.wraps(f)
        def wrapper(self, *args, **kwargs):
            for a, t in zip(args, types):
                if not isinstance(a, t):
                    raise TypeError("Expected {}, got {}".format(t, a))
            return f(self, *args, **kwargs)
        return wrapper
    return decorator

if __name__ == "__main__":
    class Test:
        @m_types_check(tuple, tuple)
        def add(self, a, b):
            return a[0] + b[1]
    a = Test()
    print(a.add((1,2), (3,4)))
