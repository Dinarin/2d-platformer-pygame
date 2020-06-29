import pygame
import pygame_gui

# Rough current performance measure - Button creation time taken: 0.200 seconds.
# (54 x rounded rectangles)



class GameButton(pygame_gui.elements.UIButton):
    def __init__(self, r_rect, text, manager, b_id_name):
        """Creates game buttons.

            Arguments:
                r_rect (tup): (relative_x, relative_y,
                                width, height).
                text (str): button text.
                manager (:obj: pygame_gui.UIManager):
                    button manager
                b_id_name (str) button unique name
        """
        super().__init__(relative_rect=pygame.Rect(r_rect), text=text,manager=manager, object_id='#' + b_id_name)

class MenuButtons(pygame.Rect):
    def __init__(self, rect, manager, p_surface):
        """Creates menu rectangles for GameButtons.

        """
        super().__init__(rect)
        self.manager = manager
        self.buttons = {}

    def create_buttons_col(self, b_dict, spacing):
        # Storing the dictionary.
        self.buttons.update(b_dict)
        b_ids = b_dict.keys()
        b_names = b_dict.values()

        # Getting the number of columns.
        num_col = len(b_ids)

        # Getting dimensions of columns.
        b_height = (self.height - spacing)/(num_col) - spacing
        b_width = self.width
        r_list = [(self.x, self.y + j * spacing + ((j - 1) * b_height),
                    b_width, b_height) for j in range(1, num_col + 1)]
        for t_rect, b_name, b_id in zip(r_list, b_names, b_ids):
            self.buttons[b_id] = GameButton(t_rect, b_name, self.manager, b_id)

#    def create_buttons_row(num,row, bg):
#        for j in range(1, num_row+1):
#            position = ((bg.get_width() - button_row_width)/2 , (j * spacing + ((j - 1) * button_row_height)))
#            GameButton((*position, button_row_width, button_row_height),
#                                 str(1) + ',' + str(j),
#                                 manager,
#                                 str(1) + ',' + str(j))

if __name__ == "__main__":
    from . import entities as e_

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
                    if event.ui_object_id == e_.w:
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
