import pygame
class Vector:
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
        return Vector(self.x*v.x, self.y*v.y)
  
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
#        self.mass = 20
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

    def apply_force(self, force):
        self.acceleration += force
        self.speed = self.base_speed + self.acceleration
        print(self.speed.get_tuple())
        self.rect.move_ip(self.speed.get_tuple())
        self.sprite.rect.move_ip(self.speed.get_tuple())
    
    def add_speed(self, vector):
        self.base_speed += vector
        self.rect.move_ip(self.speed.get_tuple())
        self.sprite.rect.move_ip(self.speed.get_tuple())

    def return_group(self):
        return self.sprite.Group1
