import pygame
import sys
import pygame.sprite
import lib.vector
import lib.classes as cl
import lib.spritesheetgaps as sp

class MainGame:
    def __init__(self, resolution):

        # initializing pygame
        pygame.init()

        # opening window
        self.screen = pygame.display.set_mode(resolution)
        self.state = 'running'
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('Game')

    def start_game(self):
        # variables
        # Temporary variables
        window_size = (1024,768)
        canvas_size = (800,600)
        circle_coords = (350,250)
        canvas_topleft = (112, 84)
        circle_dimensions = (42, 42)
        blue = (230, 255, 247)


        # Background
        bg_image = pygame.Surface(canvas_size)
        bg_image.fill((163,242,211))
        phys_dict = {
                'g': 1000.0,
                'k': 2.0
                }

        # Creating game objects
        camera = cl.GameView(canvas_topleft, canvas_size, bg_image)  # gameview
        activity = cl.GameActivity(sprites_dict, phys_dict)

        # Game cycle
        while True:
            frame_n += 1
            # Each cycle is drawing one frame

            # handling events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # catching keys from keyboard
            pressed = pygame.key.get_pressed()
            #assign_event_to keys(pressed)

            # updating game
            time_passed = self.clock.tick(30)
            time_passed_seconds = time_passed / 1000.0

            # drawing screen
            camera.find_render_group()
            changed_rects = camera.render()
            pygame.display.update(changed_rects)

if __name__ == "__main__":
    resolution = (1024,768)
    sprites_dict
    game = MainGame(resolution)
    game.start_game()
