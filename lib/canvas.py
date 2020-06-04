import pygame
class Canvas(pygame.Surface):
    """
    Main game image that will be blitted on player camera.
    ...
    Attributes
    ---------- 
    Methods
    ---------- 
    __init__(
    """
    def __init__(self, dimensions, background):
        pygame.Surface.__init__(self, dimensions)
        self.background = background
        self.blit(background, (0,0))
        self.display = background.copy()
    def draw_background(self, surface, coordinates):
        self.background.blit(surface, coordinates)

    def draw_object(self, object_rect, object_surface):
        self.fill((255,0,0))
        self.blit(object_surface, object_rect)
#        pygame.time.wait(1000)

class ObjectSurface(pygame.Surface):
    def __init__(self, dimensions, color=(0,255,0), r=20):
        pygame.Surface.__init__(self, dimensions)

        # Background transparency
        self.set_colorkey((255,0,255))  # setting magenta to be transparent
        self.fill((255,0,255))  # filling background with magenta

        # Drawing circle
        pygame.draw.circle(self, color, (50,50), r) 
