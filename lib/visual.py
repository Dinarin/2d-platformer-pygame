import pygame
import sys
import os

from lib import vector as v_
from lib import spritesheetgaps as sp
from lib import pyganim as pyganim_

# Events
# event1 = Event(type, **attributes)



#sprite_rects = {[]}
class SpriteSheet:
    def __init__(self, imgfile, colorkey=None):
        self.spritesheet = sp.spritesheet(imgfile)
        self.colorkey = colorkey
        self.images = {}
        # Modified dict
        self.modified = None
        self.zoomed = False

    # Methods that input sprites in dict attribute
    def get_strips(self, rows_dict):
        """
        Create surfaces from rows and put them into dictionary
        """
        for name in rows_dict:
            img_list = rows_dict[name]
            images = self.spritesheet.load_strip(img_list[0], img_list[1],\
                    img_list[2], self.colorkey)
            self.images[name] = []
            for image in images:
                self.images[name].append(image)

    def get_images(self, rect_dict):
        """
        Create surfaces from rects and put them into dictionary
        """
        for name in rect_dict:
            img_rect = rect_dict[name]
            imaged = self.spritesheet.get_images(img_rect, self.colorkey)
            self.images[name] = []
            for image in images:
                self.images[name].append(image)

    # Methods that return objects that were made from dict attribute
    def animate(self, images_name, delay, loop):
        """
        Make a pyganim object from a name and properties
        """
        surfaces = self.images[images_name]
        frames = []
        for surface in surfaces:
            frames.append((surface, delay))
        return pyganim_.PygAnimation(frames, loop)

    def get_images(self, *images_names):
        """
        Return list of surfaces from names
        """
        new_dict = {}
        for name in images_names:
            new_dict[name] = self.images[name]

        return self.images[images_name]

    def zoom(self, multiplier, change=False):
        """
        Zooms entire sprites dict with or without modifying it
        """
        if self.zoomed:
            raise Exception("Images were already zoomed")
        else:
            new_images = {}
            for name in self.images:
                images = self.images[name]
                new_images[name] = []
                for image in images:
                    old_size = image.get_size()
                    new_size = (int(old_size[0]*multiplier),\
                            int(old_size[1]*multiplier))
                    new_image = pygame.transform.scale(image, new_size)
                    new_images[name].append(new_image)
            if change:
                self.images = new_images
                self.zoomed = True
            else:
                self.modified = new_images

class GameView(pygame.Surface):
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
        self.blit(background, (0,0))
        self.display = background.copy()
        self.rect = pygame.Rect(coordinates, dimensions)

    # main rendering methods of the game
    def update(self, active_group):
        """
        Updates sprites that are changing
        """
        active_group.update()

    def render(self):
        """
        Returns a rect list that should be passed to pygame.display.update()
        """
        return self.render_group.draw(self)

    def find_render_group(self, activity): self.render_group = activity.get_render_group


class GameWorld:
    def __init__(self, sprites_dict, variables_dict):  # some sort of stored level data should be the arguments
        player_sprite = sprites_dict['player']
#        player1 = PlayerObject(player_sprite, )
        self.render_g = GameSpritesGroup(player1)

    def get_render_group(self):
        return self.render_g


if __name__ == "__main__":
    # Open window
    resolution = (1024,768)
    bg_color = (94,129,162)
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption('Game')
    bg_image = pygame.Surface(resolution)
    bg_image.fill(bg_color)
    screen.blit(bg_image, (0,0))
    # Clock
    clock = pygame.time.Clock()

    # images_dict have rects from imagefile and the keys are added as the spritegroup
    img_path = '../pixels/small_spritesheet_by_kenney_nl.png'
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, img_path)


    # Get images file and put name on images

    image_rows = {
            'player1': ((0,0,21,21), 5, 2),  # rect, image count, gap in pixels
            'player2': ((0,69,21,21), 5, 2)
    }
    sp = SpriteSheet(filename, colorkey=True)
    sp.get_strips(image_rows)
    sp.zoom(4)
    print(sp.images)
    new_images = sp.modified
    print(new_images)
    # Game cycle
    while True:
        # handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # updating game
        time_passed = clock.tick(30)
        time_passed_seconds = time_passed / 1000.0

        # drawing screen
        for key in new_images:
            for image in new_images[key]:
                screen.blit(image, (500,500))
                pygame.time.wait(1000)
                pygame.display.update()

        pygame.display.update()

#    level1 = Level('../pixels/small_spritesheet_by_kenney_nl.png')
#    level1.set_player_sprite((0, 0, 21, 21), colorkey=True)
#    player_sprite = level1.get_player_sprite
