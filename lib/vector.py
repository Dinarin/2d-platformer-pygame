class Vector2d:
    #    @type_check(tuple, 2)
    def __init__(self, coords):
        """
        input a tuple of (x,y)
        """
        # Type check
#        if not ((isinstance(coords, tuple)) and (len(coords) == 2)):
#            raise TypeError("{} isn't a tuple of length 2".format(coords))
        self.coords = list(coords)
        self.x = coords[0]
        self.y = coords[1]

    def __eq__(self, vec):

        # Type check
        if not isinstance(vec, Vector2d):
            raise TypeError("Argument is a {} object, not a Vector2d object".format(type(vec)))

        return self.coords == vec.coords

    def __add__(self, vec):

        # Type check
        if not isinstance(vec, Vector2d):
            raise TypeError("Argument is a {} object, not a Vector2d object".format(type(vec)))

        return Vector2d((self.x+vec.x, self.y+vec.y))

    def __mul__(self, num):

        # Type check
        if not isinstance(num, float):
            raise TypeError("Argument is a {} object, not a float object".format(type(num)))

        return Vector2d((self.x*num, self.y*num))

    def __sub__(self, vec):

        # Type check
        if not isinstance(vec, Vector2d):
            raise TypeError("Argument is a {} object, not a Vector2d object".format(type(vec)))

        return Vector2d((self.x-vec.x, self.y-vec.y))

    def __matmul__(self, vec):

        # Type check
        if not isinstance(vec, Vector2d):
            raise TypeError("Argument is a {} object, not a Vector2d object".format(type(vec)))

        return [a*b for a,b in zip(self.coords, vec.coords)]

    # reflected operators
    def __rmul__(self, num):

        # Type check
        if not isinstance(num, float):
            raise TypeError("Argument is a {} object, not a float object".format(type(num)))

        return self*num

    # in place operators
    def __iadd__(self, vec):

        # Type check
        if not isinstance(vec, Vector2d):
            raise TypeError("Argument is a {} object, not a Vector2d object".format(type(vec)))

        self.x += vec.x
        self.y += vec.y
        self.coords = [self.x, self.y]
        return self

    def __imul__(self, num):

        # Type check
        if not isinstance(num, float):
            raise TypeError("Argument is a {} object, not a float object".format(type(num)))

        self.x *= num
        self.y *= num
        self.coords = [self.x, self.y]
        return self


    def __isub__(self, vec):

        # Type check
        if not isinstance(vec, Vector2d):
            raise TypeError("Argument is a {} object, not a Vector2d object".format(type(vec)))

        self.x -= vec.x
        self.y -= vec.y
        self.coords = [self.x, self.y]
        return self

    # operators
    def __neg__(self):
        return Vector2d((self.x*(-1), self.y*(-1)))

    def __abs__(self):
        return Vector2d((abs(self.x), abs(self.y)))

    # print
    def __str__(self):
        return str(self.coords)

    def set(self, xy):
        x = xy[0]
        y = xy[1]
        self.x = x
        self.y = y


if __name__ == "__main__":
    vector2 = Vector2d((-4.0, 5.0))
    vector1 = Vector2d((3.0, 1.0))
    print(vector1)
    vector1 -= vector2
    vector1 *= 2.0
    print(-vector1)
    print(abs(vector2))
    vector1 = Vector2d('wrong'
            )
