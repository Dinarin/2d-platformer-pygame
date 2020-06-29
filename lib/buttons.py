import pygame
import pygame_gui

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
def create_buttons_col(col_len, bg):
    for j in range(1, 10):
        position = ((bg.get_width() - button_row_width)/2 , (j * spacing + ((j - 1) * button_row_height)))
        pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position,
                                                           (button_row_width,
                                                            button_row_height)),
                                 text=str(1) + ',' + str(j),
                                 manager=manager,
                                 object_id='#' + str(1) + ',' + str(j))

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
