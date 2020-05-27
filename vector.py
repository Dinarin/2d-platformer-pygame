class Vector:
    def __init__(self, x = 0.0, y = 0.0):
        sqrt = (x*x+y*y)**0.5
        self.length = sqrt
        self.x = x
        self.y = y

    def __add__(self, v1):
        self.x += v1.x
        self.y += v1.y

    def __sub__(self, v1):
        self.x -= v1.x
        self.y -= v1.y

    def normcord(self):
        self.nx = self.x/self.length
        self.ny = self.y/self.length

    def __mul__(self, a):
        self.x = self.x * a
        self.y = self.y * a
  
    def dot(self, a):
        self.dot1 = self.x * a.x + self.y * a.y

