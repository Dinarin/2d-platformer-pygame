# Source: https://www.pygame.org/wiki/Spritesheet adapted for python3 and fixed tile dimensions
# This class handles sprite sheets
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)

import pygame

class SpriteSheet(object):
    """Class for managing spritesheets.

    Args:
        filename (str): path to the spritesheet file.
        tile_size (tuple): dimensions of a tile as
            (width, height).
        gap_size (int): gap between individual
            sprites in pixels.
        border (int): spritesheet margin in pixels,
            a frame without images.

    Attributes:
        sheet (:obj:) pygame.Surface: loaded
            spritesheet image
        tile_size (tuple): dimensions of a tile as
            (width, height)
        t_width (int): tile width in pixels
        t_height (int): tile height in pixels
        gap_size (int): gap between individual sprites
            in pixels
    """

    def __init__(self, filename, tile_size, gap_size, border=None):
        try:
            spritesheet = pygame.image.load(filename).convert()
            if border is not None:
                sp_rect = spritesheet.get_rect()
                sp_x = sp_rect.width
                sp_y = sp_rect.height
                cropped_dim = (sp_x-border, sp_y-border)
                cropped_rect = pygame.Rect((border, border), cropped_dim)
                cropped = pygame.Surface(cropped_dim)
                cropped.blit(spritesheet, (0,0), area=cropped_rect)  # cropping spritesheet
                spritesheet = cropped
            self.sheet = spritesheet
            self.tile_size = tile_size
            self.t_width = tile_size[0]
            self.t_height = tile_size[1]
            self.gap_size = gap_size
        except pygame.error as message:
            raise SystemExit('Unable to load spritesheet image:{}'.format(filename), message)
    # Load a specific image from column x row y assuming first image begins at (0,0) and numeration of rows and columns begins at 0
    def image_at(self, xy, colorkey = None):
        """Get image from column x, row y.
        xy = (x, y)
        Loads image from column x row y
        """
        x_px = (self.t_height + self.gap_size) * xy[0]
        y_px = (self.t_width + self.gap_size) * xy[1]
        rectangle = (x_px, y_px, self.t_width, self.t_height)
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            image.set_colorkey(colorkey)
        return image
    # Load a whole bunch of images and return them as a list from a list of tuples [(x,y), (x,y)]
    def images_at(self, xys, colorkey = None):
        """Gets images from a list of columns and rows.

        xys = [xy1, xy2...]
        xy1 = (x, y)...
        Loads images from column x row y
        """
        return [self.image_at(xy, colorkey) for xy in xys]
    # Load a whole strip of images
    def load_strip(self, xy, image_count, colorkey = None):
        """Gets a strip of images.

            Args:
                xy
        """
        xys = [(xy[0]+x, xy[1]) for x in range(image_count)]
        return self.images_at(xys, colorkey)

if __name__ == "__main__":
    import os
    import sys
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

    # sprites_dict have rects from spritefile and the keys are added as the spritegroup
    sprites_path = '../images/small_spritesheet_by_kenney_nl.png'
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, sprites_path)


    # Get sprites file and put name on sprites
    sprite_rows = {
            'player1': ((0,0), 5),  # column, row, image count
            'player2': ((0,3), 5)
    }
    gap = 2
    border = 1
    tile = (21,21)
    sp = SpriteSheet(filename, tile, gap, border=border)
    player1 = sp.load_strip(*sprite_rows['player1'])
    player2 = sp.load_strip(*sprite_rows['player2'])
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
        for sprite in player1:
            screen.blit(sprite, (500,500))
            pygame.time.wait(1000)
            pygame.display.update()

        pygame.display.update()

