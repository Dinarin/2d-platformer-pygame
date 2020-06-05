import pygame
import math
import numbers
import decimal

class Vector2d:
    # kwargs one letter coordinate names, standard value is "val" key
    def __init__(*args):
        #self.coord = 1
        #if type(list1) == type(list):
        self.coord = list1
        #if kwargs  is not None:
        #    for key, value in kwargs.iteritems():
        #        if (key == 'val'):

    def __eq__(self, vec):
        assert isinstance(vec, VectorNd)
            if len(self.coord) is not len(vec.coord):
                raise ValueError('Dimentionality mismatch')
        return self.coord == vec.coord

    def __add__(self, vec):
        assert isinstance(vec, VectorNd)
        return VectorNd(self.coord + vec.coord)

    def __mul__(self, x):
        assert isinstance(x, float)
        return VectorNd([i * x for i in self.coord])

    def __sub__(self, vec):
        assert isinstance(vec, VectorNd)
        return VectorNd(self.coord - vec.coord)

    def __dot__(self, vec):
        if not isinstance(vec, VectorNd):
            raise ValueError('Multiplying on a not vector')
        return [a*b for a,b in zip(self.coord, vec.coord)]

    def add_(self, vec):
        old = VectorNd(self)
        assert isinstance(vec, VectorNd)
        self.coord += vec.coord
        return not VectorNd.eq(self, old)
    

    def mul_(self, x):
        old = VectorNd(self)
        assert isinstance(x, float)
        self.coord = [i * x for i in self.coord]
        return not VectorNd.eq(self, old)

    def printvec(self):
        print(self.coord)

    def __init__(self, x = 0.0, y = 0.0):
        self.length = (x*x+y*y)**0.5
        self.x = x
        self.y = y

    def __add__(self, v):
        return Vector(self.x+v.x, self.y+v.y)

    def __sub__(self, v):
        return Vector(self.x-v.x, self.y-v.y)

    def normcord(self):
        self.nx = self.x/self.length
        self.ny = self.y/self.length

    def __mul__(self, v):
        if type(v) == type(self):
            return Vector(self.x*v.x, self.y*v.y)
        elif (type(v) == 'float') or (type(v) == 'int'):
            return Vector(self.x*v, self.y*v)
  
    def dot(self, v):
        return self.x * v.x + self.y * v.y

    def get_tuple(self):
        return (self.x,self.y)

    def abs(self, axis):
        # 0 - x
        # 1 - y
        if not axis:
            if self.x < 0:
                return -self.x
            else:
                return self.x
        if axis:
            if self.y < 0:
                return -self.y
            else:
                return self.y


class GameObject():
    def __init__(self, coordinates, dimensions):
#        pygame.Rect.__init__(self, coordinates, dimensions)
        self.mass = 20.0
        self.speed = Vector()
        self.base_speed = Vector()
        self.acceleration = Vector()
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
        self.speed += (1/self.mass * g_acceleration) * delta_t
        self.rect.y += self.speed * dt

    # Updating Rect objects

    def update_state(self):
        self.sprite.rect.move_ip(self.rect)

    # Rendering
    def return_group(self):
        return self.sprite.Group1
