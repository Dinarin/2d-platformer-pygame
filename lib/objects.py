import pygame
import math
import numbers
import decimal

class Vector2d:
    def __init__(self, x=0.0, y=0.0):
        self.coord = [x, y]

    def __eq__(self, vec):
        assert isinstance(vec, Vector2d)
#            if len(self.coord) is not len(vec.coord):
#                raise ValueError('Dimentionality mismatch')
        return self.coord == vec.coord

    def __add__(self, vec):
        assert isinstance(vec, Vector2d)
        return Vector2d(self.coord + vec.coord)

    def __mul__(self, x):
        assert isinstance(x, float)
        return Vector2d([self.coord[0] * x, self.coord[1] * x])

    def __sub__(self, vec):
        assert isinstance(vec, Vector2d)
        return Vector2d(self.coord - vec.coord)

    def __dot__(self, vec):
        if not isinstance(vec, Vector2d):
            raise ValueError('Multiplying on a not vector')
        return [a*b for a,b in zip(self.coord, vec.coord)]

    def add_(self, vec):
        old = Vector2d(self)
        assert isinstance(vec, Vector2d)
        self.coord += vec.coord
        return not Vector2d.eq(self, old)
    

    def mul_(self, x):
        old = Vector2d(self)
        assert isinstance(x, float)
        self.coord = [self.coord[0] * x, self.coord[1] * x]
        return not Vector2d.eq(self, old)

    def get_tuple(self):
        print(self.coord)

#    def __init__(self, x = 0.0, y = 0.0):
#        self.length = (x*x+y*y)**0.5
#        self.x = x
#        self.y = y
#
#    def __add__(self, v):
#        return Vector(self.x+v.x, self.y+v.y)
#
#    def __sub__(self, v):
#        return Vector(self.x-v.x, self.y-v.y)
#
#    def normcord(self):
#        self.nx = self.x/self.length
#        self.ny = self.y/self.length
#
#    def __mul__(self, v):
#        if type(v) == type(self):
#            return Vector(self.x*v.x, self.y*v.y)
#        elif (type(v) == 'float') or (type(v) == 'int'):
#            return Vector(self.x*v, self.y*v)
#  
#    def dot(self, v):
#        return self.x * v.x + self.y * v.y


class GameObject():
    def __init__(self, coordinates, dimensions):
#        pygame.Rect.__init__(self, coordinates, dimensions)
        self.mass = 20.0
        self.speed = Vector2d()
        self.base_speed = Vector2d()
        self.acceleration = Vector2d()
        self.rect = pygame.Rect((0,0), dimensions)
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.Surface(dimensions)
        self.sprite.rect = self.sprite.image.get_rect()

        print("RECT", self.rect)
        print("SPRITERECT", self.sprite.rect)
        # Background transparency
#        self.sprite.image.set_colorkey((255,0,255))  # setting magenta to be transparent
        self.sprite.image.fill((255,0,255))  # filling background with magenta
        self.sprite.rect = self.sprite.image.get_rect()

        # Drawing circle
        self.sprite.Group1 = pygame.sprite.Group(self.sprite)
    
    def set_circle_sprite(self):
        color=(0, 53, 255)
        r = 20
        pygame.draw.circle(self.sprite.image, color, (21,21), r) 

    # Physics

    def apply_force(self, force):
        self.acceleration += force
        self.speed = self.base_speed + self.acceleration
        print(self.speed.get_tuple())
            
    def add_momentum(self, vector):
        self.speed += vector

    def update_obj_physics(self, delta_t, g_acceleration):
        print(type(1/self.mass))
        print(type(delta_t))
        self.speed += (g_acceleration * 1/self.mass) * delta_t
        self.rect.y += self.speed * dt

    # Updating Rect objects

    def update_state(self):
        self.sprite.rect.move_ip(self.rect)

    # Rendering
    def return_group(self):
        return self.sprite.Group1
