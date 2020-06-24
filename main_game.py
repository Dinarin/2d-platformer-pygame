import pygame
import sys
import os
from lib import visual as vi_
from lib import vector as v_
from lib import spritesheetgaps as sp_
from lib import pyganim as anim_
from lib import levels as l_
from lib import entities as e_
#from levels import levels as dicts_


def start_game():

    # Open window
    resolution = (1008,1008)
    bg_color = (0,35,69)
    colorkey = (94,129,162)
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption('Game')
    bg_image = pygame.Surface(resolution)
    bg_image.fill(bg_color)
    screen.blit(bg_image, (0,0))
    # Clock
    clock = pygame.time.Clock()

    # images_dict have rects from imagefile and the keys are added as the spritegroup
    img_path = './images/small_spritesheet_by_kenney_nl.png'
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, img_path)


    # Get images file and put name on images
    tile_size = (21,21)
    gap = 2
    border = 1
    image_rows = {
            'p1_run_right': ((2,0), 2),  # rect, image count
            'p2_run_right': ((2,3), 2)
    }
    images = {
         'p1_idle': [(20,0)],# list of tuples
         'p2_idle': [(20,3)]
        }
    lvl_img = {
        'player1': {
            'run_left': 'p1_run_left',
            'run_right': 'p1_run_right',
            'idle': 'p1_idle'
            },
        'player2': {
            'run_left': 'p2_run_left',
            'run_right': 'p2_run_right',
            'idle': 'p2_idle'
            }
    }

    # controls dicts
    controls = [{
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'up': pygame.K_UP,
            'down': pygame.K_DOWN
            },
            {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'up': pygame.K_w,
            'down': pygame.K_s
            }
            ]

    # Loading images from spritesheet
    ip = vi_.ImagePicker(filename, tile_size, gap, border, colorkey=colorkey)
    ip.get_strips(image_rows)
    ip.get_images(images)
    ip.flip('p1_run_right','p1_run_left')
    ip.flip('p2_run_right','p2_run_left')
    # zooming before animating
    ip.zoom_dict(2)

    # animations
    delay = 0.2
    animations_list = [
            'p1_run_right','p1_run_left','p2_run_right','p2_run_left'
            ]
    for animation in animations_list:
        ip.animate(animation, delay)
    new_images = ip.modified

    li = vi_.LevelImages(new_images, lvl_img, *ip.return_zoom_param())

    # Building level 0
    dim = (24,24)
    Level0 = l_.LevelData(dim, li)
    Level0.load_map(0)
    Level0.parse_map()
    world = e_.World(Level0)
    world.add_players(['player1','player2'])
#    world.add_tiles(GameTiles, 'grass')

    # Adding objects not present in world:
    game_border = e_.GameBorders((0,0,*resolution))

    # SpritesGroup setup
    player_sprites = e_.GameSpritesGroup()
    player_dict = world.get_players()
    i = 0
    for key in player_dict:
        player=player_dict[key]
        player.set_controls(controls[i])
        player.set_colliding_list(game_border, player_sprites)
        player_sprites.add_sprite(player)
        i+=1

    all_sprites = e_.GameSpritesGroup(player_sprites.sprites())

    # Game cycle
    while True:
        # updating game
        time_passed = clock.tick(30)

        # handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pressed = pygame.key.get_pressed()
        # for debugging
#        for key in player_dict:
#            player=player_dict[key]

        # drawing all sprites
        player_sprites.clear(screen, bg_image)
        player_sprites.update(pressed)
        changed_rects = player_sprites.draw(screen)
        pygame.display.update()

start_game()
