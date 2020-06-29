import pygame
import pygame_gui
from lib.entities import *

# Rough current performance measure - Button creation time taken: 0.200 seconds.
# (54 x rounded rectangles)


pygame.init()


pygame.display.set_caption('Button Theming Test')
window_surface = pygame.display.set_mode((800, 600))
# Setting string variables.
theme_path = './lib/buttons.json'


manager = pygame_gui.UIManager((800, 600), theme_path)
clock = pygame.time.Clock()

background = pygame.Surface((800, 600))
background.fill(manager.get_theme().get_colour('dark_bg'))

load_time_1 = clock.tick()

button_row_width = 200
button_row_height = 50
spacing = 20
class GameButton(pygame_gui.elements.UIButton):
    def __init__(self, r_rect, text, manager, b_id_name):
        """Creates game buttons.

            Arguments:
                r_rect (tup): (relative_x, relative_y,
                                width, height).
                text (str): button text.
                manager (:obj: pygame_gui.UIManager):
                    button manager
                b_id_name (str) button id without '#'
        """
        super().__init__(relative_rect=pygame.Rect(r_rect), text=text,
                                manager=manager, object_id='#' + b_id_name)

def create_buttons_col(col_len, bg):
    for j in range(1, col_len+1):
        position = ((bg.get_width() - button_row_width)/2 , (j * spacing + ((j - 1) * button_row_height)))
        GameButton((*position, button_row_width, button_row_height),
                             str(1) + ',' + str(j),
                             manager,
                             str(1) + ',' + str(j))

def GameMenus(pygame.sprite.DirtySprite)
create_buttons_col(4, background)
load_time_2 = clock.tick()
print('Button creation time taken:', load_time_2/1000.0, 'seconds.')

is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
