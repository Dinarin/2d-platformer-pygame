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
    def __init__(self, coordinates, dimensions, background):
        pygame.Surface.__init__(self, dimensions)
        self.background = background
        self.blit(background, (0,0))
        self.display = background.copy()
        self.rect = pygame.Rect(coordinates, dimensions)
    def draw_background(self, surface, coordinates):
        self.background.blit(surface, coordinates)

    def draw_object(self, game_object):
        game_object.return_group().clear(self, self.background)
        game_object.return_group().draw(self)
#        pygame.time.wait(1000)
