import pygame
import sys
import os
from lib import visual as vi_
from lib import vector as v_
from lib import spritesheetgaps as sp_
from lib import pyganim as anim_
from lib import levels as l_
from lib import meta
from lib import entities as e_
from levels import tilesets as ts_



def load_images():
    colorkey = (94,129,162)
    tile_dim = (21,21)
    gap = 2
    border = 2

    # Setting string variables.
    bg_path = './images/background.png'
    img_path = './images/spritesheet_by_kenney_nl.png'

    # Finding full paths to image files no matter what folder we are in.
    dirname = os.path.dirname(__file__)
    bg_f_path = os.path.join(dirname, bg_path)
    img_f_path = os.path.join(dirname, img_path)

    # Loading tilesets dictionaries from file.
    images = ts_.get_dicts('img')
    image_rows = ts_.get_dicts('rows')
    lvl_img = ts_.get_dicts('level')

    # Generating images for the game.
    # Loading images from spritesheet.
    ip = vi_.ImagePicker(img_f_path, tile_dim, gap, border, colorkey=colorkey)
    ip.get_strips(image_rows)
    ip.get_images(images)
    ip.flip('p1_run_right','p1_run_left')
    ip.flip('p2_run_right','p2_run_left')
    ip.flip('p1_jump_right','p1_jump_left')
    ip.flip('p2_jump_right','p2_jump_left')
    ip.zoom_dict(2)  # zooming _before_ animating

    # Generating animations images.
    delay = 0.25
    animations_list = [
            'p1_run_right','p1_run_left','p2_run_right','p2_run_left',
            'p1_jump_right','p1_jump_left','p2_jump_right','p2_jump_left',
            ]
    for animation in animations_list:
        ip.animate(animation, delay)
    new_images = ip.modified

def game_update():
    # Cycling through players.
    if not game_over:
        for p_id in player_dict:
            player=player_dict[p_id]
            player.collect(bonuses_sprites)
            # print('player {} score {}, place {}'.format(key, player.score, (player.rect.x, player.rect.y)))
            event = player.global_events['game']
            world.texts[p_id].set_text("Player {}: {}".format(p_id+1, player.score))
            if event is not None:
                if event == 'end':
                    result = world.check_scores()
                    world.add_text(e_.GameText, (500, 500, 2, 2), font, text_color2, size=32)
                    result_text = world.texts[2]
                    if result == 0:
                        result_text.set_text("It's a draw!")
                    else:
                        result_text.change_color(text_color[p_id])
                        result_text.set_text("Player {} wins".format(result))
                    result_text.rect.center = (504,504)

                    all_sprites.add(world.texts[2])
                    game_over = True
                    break

def sprites_update():
    if not game_over:
            player_sprites.update()


def get_player_keys():
    for p_id in player_dict:
        player = player_dict[p_id]
        player.get_keys(e)

def start_game():
    # Assigning necessary values to variables.
    # Setting number variables.
    screen_resolutions = [(640,360), (1024,576), (1280,720)]
    game_resolutions = [(300, 300), (400, 400), (600,600)]
    menu_resolutions = [(210,300), (300,400), (400, 600)]
    resolution = (1008,1008)
    bg_color = (0,35,69)
    spacing = 5

    main_menu_b = {
            'start': 'Game Start',
            'settings': 'Settings',
            'quit': 'Exit'
            }

    # Setting dictionaries with player controls.
    controls = [{
            'left': pygame.K_a,
            'right': pygame.K_d,
            'up': pygame.K_w,
            'down': pygame.K_s
            },
            {
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'up': pygame.K_UP,
            'down': pygame.K_DOWN
            }]

    # Pygame begins.
    # Opening pygame window and writing window name.
    pygame.init()

    pygame.display.init()
    pygame.freetype.init()

    # Initializing display and setting caption.    pygame.display.init()
    pygame.display.set_caption('Pygame platformer')

    # Checking acceptable resolutions.
    screen_resolution = None
    screen_info = pygame.display.Info()
    for s_res, g_res, m_res in zip(screen_resolutions, game_resolutions,
                                    menu_resolutions):
        if (screen_info.current_h >= s_res[1]):
            screen_resolution = s_res
            game_resolution = g_res
            menu_resolution = m_res
    if screen_resolution is None:
        raise Exception(("Screen resolution {}×{} px is too "\
                "small.".format(screen_info.current_w, screen_info.current_h)))

    # Creating window.
    screen = pygame.display.set_mode(screen_resolution)
    main_view = vi_.GameScreen(screen_resolution)
    main_view.set_bg_color((100,0,100))

    w_width, w_height = screen_resolution[0], screen_resolution[1]
    main_menu = e_.GameMenus((0, 0, *menu_resolution))
    buttons1 = main_menu.create_button_area((0,0, menu_resolution[0], menu_resolution[1]))
    buttons1.center = main_view.rect.center
    active_windows = e_.GameSpritesGroup(main_menu)
    buttons1.create_buttons_col(main_menu_b, spacing)

    # Creating pygame clock object.
    clock = pygame.time.Clock()
    is_running = True
    # Game starts.
    while is_running:
        # Counting time between frames.
        time_passed = clock.tick(30)/1000.0

        # Event handling.
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                is_running = False
            # if game is running
#            get_player_keys()
            main_menu.manager.process_events(e)
        main_menu.manager.update(time_passed)

        # Drawing all sprites on the display.
        # Clearing all sprites.
        active_windows.clear(main_view.image, main_view.background)

        # Drawing all sprites.
        main_menu.manager.draw_ui(main_menu.image)
#        main_menu.debug()
        changed_rects = active_windows.draw(main_view.image, main_view.background)

        # Scaling the image down.
        new_image = pygame.transform.smoothscale(main_view.image, screen_resolution)
        screen.blit(new_image, (0,0))

        # Updating the display.
        pygame.display.update()

def start_level(resolution, l_num=1):
    game_view = vi_.GameScreen(resolution)
    game_over = False
    map_dim = (24,24)  # level map dimensions

    # Loading background image and scaling it to resolution.
    bg_image_small = pygame.image.load(bg_f_path)
    bg_image = pygame.transform.scale(bg_image_small, resolution)
    game_view.set_bg_image(bg_image)

    # Generating level data from maps and images.
    li = vi_.LevelImages(new_images, lvl_img, *ip.return_zoom_param())
    Level = l_.LevelData(map_dim, li)

    # Creating level data object
    # reading level number from command line
    lvl_num = '1'
    if (len(sys.argv) == 2) and (sys.argv[1].isnumeric()):
        if sys.argv[1] in Level.valid_maps:
            lvl_num = sys.argv[1]
        else:
            raise Exception("No valid level numbered {}".format(sys.argv[1]))

    # Loading map.
    Level.load_map(lvl_num)
    Level.parse_map()


    # Generating world. Adding objects.
    world = e_.World(Level)
    world.add_players(['player1','player2'])
    world.add_entities(e_.StaticBonus, 'bonus')
    world.add_tiles('floating_tile', 'snow')
    world.add_tiles('ground_tile', 'snow')
    game_border = e_.GameBorders((0,0,*resolution))


    # Adding objects to sprites groups.
    # Adding bonuses sprites to group.
    bonuses_dict = world.get_entities()
    bonuses_sprites = e_.ItemGroup()
    for e_id in bonuses_dict:
        bonus = bonuses_dict[e_id]
        bonuses_sprites.add_sprite(bonus)
    # All bonuses sprites are in the group, can count how much there are.
    bonuses_sprites.count_visible()

    # Adding tiles sprites to group.
    tiles_list = world.get_tiles()
    tiles_sprites = e_.GameSpritesGroup(*tiles_list)

    # Adding player sprites to group.
    # Player 1 has p_id = 0.
    # Player 2 has p_id = 1.
    player_dict = world.get_players()
    player_sprites = e_.GameSpritesGroup()
    for p_id in player_dict:
        player=player_dict[p_id]
        player.set_controls(controls[p_id])
        player.set_colliding_list(game_border, tiles_sprites, player_sprites)
        player_sprites.add_sprite(player)

    # Adding text sprites.
    font = e_.GameFont()
    text_color = ((30, 167, 255), (255, 204, 0))   # blue and yellow
    text_color2 = (232, 106, 23)  # red
    world.add_text(e_.GameText, (500, 500, 2, 2), font, text_color[0], align=1, size=16)
    world.add_text(e_.GameText, (500, 500, 2, 2), font, text_color[1], align=2, size=16)

    text_sprites = e_.GameSpritesGroup(*world.texts)

    world.texts[0].set_text('Player 1: {}'.format(player_dict[0].score))

    world.texts[1].set_text('Player 2: {}'.format(player_dict[1].score))



    # Creating groups containing sprites from different groups.
    all_sprites = e_.GameSpritesGroup(*text_sprites.sprites(), *player_sprites.sprites(), *tiles_sprites.sprites(), *bonuses_sprites.sprites())
    non_player_sprites = e_.GameSpritesGroup(*tiles_sprites.sprites(), *text_sprites.sprites(), *bonuses_sprites.sprites())

start_game()
