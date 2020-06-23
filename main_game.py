import pygame
import sys
import os

from lib import visual as vi_
from lib import vector as v_
from lib import spritesheetgaps as sp_
from lib import pyganim as anim_


def start_game(resolution):

    # initializing pygame
    pygame.init()

    # opening window
    screen = pygame.display.set_mode(resolution)
    state = 'running'
    clock = pygame.time.Clock()

    pygame.display.set_caption('Game')

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

    # Physical constants
    phys_dict = {
            'g': 1000.0,
            'k': 2.0
            }

    # Creating game objects
    camera = vi_.GameView(canvas_topleft, canvas_size, bg_image)  # gameview
    activity = vi_.GameWorld(sprites_dict, phys_dict)

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
        time_passed = clock.tick(30)
        time_passed_seconds = time_passed / 1000.0

        # drawing screen
        camera.find_render_group()
        changed_rects = camera.render()
        pygame.display.update(changed_rects)

if __name__ == "__main__":
    resolution = (1024,768)
    start_game(resolution)
