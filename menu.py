import pygame
import pygame_gui
from lib import buttons as b_
# Rough current performance measure - Button creation time taken: 0.200 seconds.
# (54 x rounded rectangles)



from lib import entities as e_

main_menu_b = {
        'start': 'Game Start',
        'settings': 'Settings',
        'quit': 'Exit'
        }
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

rectangle = (300, 10, 500, 500)
main_menu = e_.GameMenus(rectangle, manager)
main_menu.create_button_area((50, 10, 300, 200))
main_menu.b_areas[0].create_buttons_col(main_menu_b, spacing)
print(main_menu.b_areas[0].buttons.keys())
m_buttons = main_menu.b_areas[0]

m_buttons.buttons['start']
load_time_2 = clock.tick()
print('Button creation time taken:', load_time_2/1000.0, 'seconds.')

is_running = True

while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_object_id == '#start':
                    print("Start Game")
                if event.ui_object_id == '#settings':
                    print("Settings")
                if event.ui_object_id == '#quit':
                    is_running = False

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(main_menu.image)
    main_menu.debug()
    window_surface.blit(main_menu.image, (0,0))
    pygame.display.update()
