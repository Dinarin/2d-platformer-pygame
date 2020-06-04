import pygame
class Vector:
    def __init__(self, x = 0.0, y = 0.0):
        self.length = (x*x+y*y)**0.5
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

    def get_tuple(self):
        return (self.x,self.y)

class RectObject(pygame.Rect):
    def __init__(self, coordinates, dimensions):
        pygame.Rect.__init__(self, coordinates, dimensions)
    
    def move_self(self, vector):
        self.move_ip(vector.get_tuple())

    def collide_line_check(self, line):

        clipped_line = self.clipline(line)

        if clipped_line:
            # If clipped_line is not an empty tuple then the line
            # collides/overlaps with the rect. The returned value contains
            # the endpoints of the clipped line.
            return True
        else:
            return False

    def collide_line_measure(self, line):

        clipped_line = self.clipline(line)

        if clipped_line:
            # If clipped_line is not an empty tuple then the line
            # collides/overlaps with the rect. The returned value contains
            # the endpoints of the clipped line.
            start, end = clipped_line
            x1, y1 = start
            x2, y2 = end
    
