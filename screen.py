class GameScreen:
    """
    Main game screen that is shown in the game window.
    ...
    Attributes
    ----------
    Methods
    ----------
    """
    def __init__(self):
        self.screen = pygame.display.set_mode()

    def update(self, updated_canvas):
        self.screen.blit(updated_canvas)
