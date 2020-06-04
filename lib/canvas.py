import pygame
class Canvas(pygame.Surface):
    """
    Main game image that is blitted on player camera.
    ...
    Attributes
    ---------- 
    Methods
    ---------- 
    __init__(
    """
    def __init__(self, dimensions):
        blue = (0,0,255)
        pygame.Surface.__init__(self, dimensions)
        self.fill(blue)

class ObjectSprite(pygame.sprite.Sprite):
    def __init__(self, coordinate
