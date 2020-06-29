import pygame
import sys
import os

from lib import vector as v_
from lib import spritesheetgaps as sp
from lib import pyganim as pyganim_


class ImagePicker:
    """Finds images in the spritesheet.

        Args:
            imgpath (str): path to the spritesheet image.
            tile_size (tuple): dimensions of a tile
                (width, height).
            gap_size (int): gap between sprites in spritesheet
                in pixels.
            border (int): spritesheet offset in pixels.
            colorkey (tuple): RGB values of the colorkey.

        Attributes:
            spritesheet (:obj: spritesheetgaps.Spritesheet):
            colorkey (tuple): RGB values of the colorkey.
    """
    def __init__(self, imgpath, tile_size, gap_size, border=None, colorkey=None):
        self.spritesheet = sp.SpriteSheet(imgpath, tile_size, gap_size, border=border)
        self.colorkey = colorkey
        self.images = {}
        # Modified dict
        self.modified = {}
        self.animations = {}
        self.t_size = tile_size
        self.t_modified = None
        self.zoom = None

    def zoom_image(self, surface):
        # Can't zoom before the dict was zoomed
        if self.zoom is not None:
            multiplier = self.zoom
            old_size = surface.get_size()
            new_size = (int(old_size[0]*multiplier),\
                int(old_size[1]*multiplier))
            return pygame.transform.scale(surface, new_size)
        else:
            raise Exception("Should zoom entire dict before zooming\
                        images")

    # Methods that input sprites in dict attribute
    def get_strips(self, rows_dict):
        """Create surfaces from rows and put them into dictionary.
        """
        for name in rows_dict:
            img_list = rows_dict[name]
            images = self.spritesheet.load_strip(*img_list, self.colorkey)
            self.images[name] = []
            for image in images:
                # if dict is zoomed, zoom the image too
                if self.zoom is not None:
                    new_image = self.zoom_image(image)
                    self.modified[name].append(new_image)
                self.images[name].append(image)

    def get_images(self, xy_dict):
        """Create surfaces from rects and put them into dictionary.
        """
        for name in xy_dict:
            img_xy = xy_dict[name]
            images = self.spritesheet.images_at(img_xy, self.colorkey)
            self.images[name] = []
            for image in images:
                # if dict is zoomed, zoom the image too
                if self.zoom is not None:
                    new_image = self.zoom_image(image)
                    self.modified[name].append(new_image)
                self.images[name].append(image)

    # Methods that return objects that were made from dict attribute
    def animate(self, images_name, delay, loop=True):
        """Make a pyganim object from a name and properties.
        """
        surfaces = self.modified[images_name]
        frames = []
        for surface in surfaces:
            frames.append((surface, delay))
        self.modified[images_name] = pyganim_.PygAnimation(frames, loop)

    def return_images(self, *images_names, zoomed=True):
        """Return list of surfaces from names.
        """
        if zoomed:
            images = self.modified
        else:
            images = self.images
        new_dict = {}
        # Returns only names that were arguments
        for name in images_names:
            new_dict[name] = images[name]
        return new_dict

    def return_zoom_param(self):
        """Returns zoom and tile_size.
        """
        if self.zoom is not None:
            return (self.t_modified, self.zoom)
        else:
            raise Exception("Dictionary wasn't zoomed")

    def zoom_dict(self, multiplier):
        """Zooms entire sprite dict without modifying it.
        """
        self.zoom = multiplier
        self.t_modified = (int(self.t_size[0]*multiplier), \
                int(self.t_size[1]*multiplier))
        new_images = {}
        for name in self.images:
            images = self.images[name]
            new_images[name] = []
            for image in images:
                new_image = self.zoom_image(image)
                new_images[name].append(new_image)
        self.modified = new_images

    def flip(self, old_name, new_name, hor=True):
        """Flips images horizontally or vertically, calls them a new name and adds to dict.
        """
        if hor:
            bools = (True, False)
        else:
            bools = (False, True)
        new_list = [pygame.transform.flip(image, *bools) \
                    for image in self.images[old_name]]
        self.images[new_name] = new_list


class LevelImages:
    """Stores surfaces of a level
        Args:
            img_dict (dict): is a dictionary
                received from ImagePicker instance,
                that assigns lists of surfaces or
                single pyganim objects to a
                unique string
            lvl_dict (dict): is a dictionary that
                assigns a unique name from img_dict
                to a game object name
            zoom (int): is passed from ImagePicker

        Attributes:
            obj_dict is a dictionary that assigns lists of surfaces or pyganim objects to a game object name.
    """
    players = ['player1', 'player2']
    def __init__(self, img_dict, lvl_dict, tile_size, zoom=None):

        self.zoom = zoom
        self.tile_size = tile_size
        lvl_obj = {}
        for obj in lvl_dict:
            # creating empty dictionary for every object
            lvl_obj[obj] = {}
            for state in lvl_dict[obj]:
                # filling object dictionary with
                # corresponding surfaces
                img_name = lvl_dict[obj][state]
                lvl_obj[obj][state] = img_dict[img_name]
        self.obj_dict = lvl_obj

    def get_obj(self, obj):
        """Returns dictionary with surfaces of the object

        """
        return self.obj_dict[obj]

class GameScreen(pygame.sprite.Sprite):
    """Class for game screen surface.
        Args:
            dimensions (tup): (width, height)
    """
    def __init__(self, dimensions):
        super().__init__()
        self.image = pygame.Surface(dimensions)
        self.background = None

    def set_bg_color(self, color):
        self.image.fill(color)
        self.background = self.image.copy()

    def set_bg_image(self, image):
        self.image.blit(image, (0, 0))
        self.background = self.image.copy()


if __name__ == "__main__":
    # Open window
    resolution = (1008,1008)
    bg_color = (94,129,162)
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption('Game')
    bg_image = pygame.Surface(resolution)
    bg_image.fill(bg_color)
    screen.blit(bg_image, (0,0))
    # Clock
    clock = pygame.time.Clock()

    # images_dict have rects from imagefile and the keys are added as the spritegroup
    img_path = '../images/small_spritesheet_by_kenney_nl.png'
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, img_path)


    # Get images file and put name on images
    tile_size = (21,21)
    gap = 2
    border = 1
    image_rows = {
            'p1_run_right': ((0,0), 5),  # rect, image count
            'p2_run_right': ((0,3), 5)
    }
    lvl_dict = {
    'player1': {
                'run_left': 'p1_run_left'}
    }

    sp = ImagePicker(filename, tile_size, gap, border, colorkey=True)
    sp.get_strips(image_rows)
    sp.flip('p1_run_right','p1_run_left')
    sp.zoom(2)
    ls = LevelImages(sp.images, lvl_dict)
    new_images = sp.modified
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
