import pygame
import sys
import os
from lib import visual as vi_
from lib import vector as v_
from lib import spritesheetgaps as sp_
from lib import pyganim as anim_
from lib import levels as l_

# Events
# event1 = Event(type, **attributes)
class World:
    """
    Adds entities according to level data
    """

    def __init__(self, level_data):
        """
        img_dict is a dictionary received from ImagePicker,that assigns
            lists of surfaces or single pyganim objects to a unique name
        lvl_dict is a dictionary that assigns a unique name from
            img_dict to a game object name
        self.obj_dict is a dictionary that assigns lists of surfaces or pyganim objects to a game object name
        """

        # Preparing to track objects
        self.entities = {}
        self.tiles = []
        self.entity_id = 0
        self.players = {}

        # Storing level data
        self.obj_dict = level_data.obj_map  # stores what coordinates do objects have
        self.imgs = level_data.lvl_img  # store LevelImages

        # width and height in tiles
        self.width = level_data.dim[0]
        self.height = level_data.dim[1]

        # Getting tile size
        self.tile_size = self.imgs.tile_size

    def xy_to_rect(self, xy):
        t_width = self.tile_size[0]
        t_height = self.tile_size[1]
        x_px = xy[0]*t_width
        y_px = xy[1]*t_height
        return (x_px, y_px, t_width, t_height)

    # Managing entities
    def add_tiles(self, TileClass, tile_name):
        xys = self.obj_dict[tile_name]
        img_dict = self.imgs.get_obj(tile_name)
        for xy in xys:
            rect = self.xy_to_rect(xy)
            self.tiles.append(TileClass(rect, img_dict))


    def add_players(self, player_images_list):
        i = 0
        for player_image_name in player_images_list:
            xy = self.obj_dict['player'][i]
            img_dict = self.imgs.get_obj(player_image_name)
            rect = self.xy_to_rect(xy)
            self.players[i] = PlayerEntities(rect, img_dict)
            i += 1

    def add_entities(self, EntityClass, entity_name):
        xy = self.obj_dict[entity_name]
        img_dict = self.imgs.get_obj(entity_name)
        # Stores the entity then advances the current id
        for xy in xys:
            rect = self.xy_to_rect(xy)
            self.entities[self.entity_id] = EntityClass(rect, img_dict)
            entity.id = self.entity_id
            self.entity_id += 1


    def get_tiles(self):
        return self.tiles

    def get_entities(self):
        return self.entities

    def get_players(self):
        return self.players


class GameSpritesGroup(pygame.sprite.RenderUpdates):

    def __init__(self, *sprites):
        # constructor
        super().__init__(*sprites)

    def update_objects(self):
        self.update(args)

    #?
    def add_sprite(self, sprite):
        self.add(sprite)


class GameObjects(pygame.sprite.DirtySprite):
    def __init__(self, rect, img_dict):
        """
        Class for game objects
        dim - (height, width)
        pic - Surface with image
        Objects' coordinates are initially (0,0)
        """
        super().__init__()

        #DirtySprite attributes
        self.dirty = False
        self.visible = True

        # Setting game object attributes
        #self._quality = object_dict['quality']

        # Setting sprite attributes
        self.image = None
        self.rect = pygame.Rect(rect)
        self.images = img_dict

    def move(self):
        pass

    def update(self):  # drawing method
        pass

    def set_sprite(self):
        pass

class GameTiles(GameObjects):
    def __init__(self):
        pass

class GameEntities(GameObjects):
    def __init__(self, rect, img_dict):
        """
        Class for game objects
        dim - (height, width)
        pic - Surface with image
        Objects' coordinates are initially (0,0)
        """
        super().__init__(rect, img_dict)

        #DirtySprite attributes
        self.dirty = False
        self.visible = True

        # Setting game object attributes
        #self._quality = object_dict['quality']

        # Setting sprite attributes
        self.image = None
        self.images = img_dict
        self.sprites = None

    def move(self):
        pass

    def update(self):  # drawing method
        pass

    def set_sprite(self):
        pass

class InteractiveEntities(GameEntities):
    def __init__(self, rect, img_dict):
        """
        Class for interactive game objects
        assumes that dimensions are the same is the picture
        Objects' coordinates are initially (0,0)
        """
        super().__init__(rect, img_dict)

    def get_any_group_colision(self, group):
        """
        Returns one random collided Sprite object
        Doesn't change the group
        """
        return pygame.sprite.spritecollideany(self, group, False)

    def get_all_group_colisions(self, group):
        """
        Returns a list of all collided Sprite objects
        Doesn't change the group
        """
        return pygame.sprite.spritecollide(self, group, False)

    def get_rect(self):
        return self.rect

    def update(self):
        pass

class MovingEntities(GameEntities):
    def __init__(self, rect, img_dict):
        """
        Class for moving game objects
        Objects' coordinates are initially (0,0)
        """
        super().__init__(rect, img_dict)

    def set_speed(self, new_speed):
        self.speed = new_speed

    def move(self):
        pass

    def update(self):
        pass


class GravityEntities(MovingEntities):
    def __init__(self, rect, img_dict):
        """
        Class for moving game objects that obey gravity
        Objects' coordinates are initially (0,0)
        """
        super().__init__(rect, img_dict)

        # attributes
        self.gravity = True
        self.last_hline = None  # attribute that stores horizontal line

        # Attributes methods
    def get_mass(self):
        return self.mass

    def set_mass(self, new_mass):
        self.mass = new_mass

    def set_speed(self, new_speed):
        self.speed = new_speed

    # Physics
    def is_in_between_x(self, x_left, x_right):
        if (self.rect.left > x_left) and (self.rect.right < x_right):
            return True
        else:
            return False

    def is_on_floor(self):
        y_line = self.last_hline[0][1]
        x1 = self.last_hline[0][0]
        x2 = self.last_hline[1][0]
        if (self.rect.bottom == y_line) and self.is_in_between_x(x1, x2):
            return True
        else:
            return False

    def apply_force(self, force):
        self.acceleration += force
        self.speed = self.base_speed + self.acceleration

    def move(self, time):
        if self.is_on_floor == False:
            self.speed += (g_acceleration * (1/self.mass)) * delta_t
            self.rect.y += self.speed.y * delta_t
        else:
            self.acceleration = 0.0
            self.v.y = 0.0
        self.speed = time * self.v.x * k
        self.v.y -= delta * self.v.y * k - gt
        self.rect.centerx += self.v.x * delta
        self.rect.centery += self.v.y * delta


#    def update(self, delta, g, k):

class PhysicalEntities(InteractiveEntities):
    def __init__(self, rect, img_dict):
        """
        Class for game objects that have impassable borders
        assumes that dimensions are the same is the picture
        Objects' coordinates are initially (0,0)
        """
        super().__init__(rect, img_dict)

    def update_rect(self, delta_t, g_acceleration):
        pass
    def update(self):
        pass

    def bounce_off_left(self, left_line):
        """
        line is a list object of a line ((x1, y1), (x2, y2))
        """
        x_left = left_line[0][0]
        if self.rect.left < x_left:
            self.v.x = abs(self.v.x)  # turn speed to the right
            self.rect.left = x_left

    def bounce_off_right(self, right_line):
        """
        line is a list object of a line ((x1, y1), (x2, y2))
        """
        x_right = right_line[0][0]
        if self.rect.right > x_right:
            self.v.x = -abs(self.v.x)  # turn speed to the left
            self.rect.right = x_right

    def bounce_off_top(self, top_line):
        """
        line is a list object of a line ((x1, y1), (x2, y2))
        """
        y_top = top_line[0][1]
        if self.rect.top < y_top:
            self.v.y = abs(self.v.y) # turn speed down
            self.rect.top = y_top

    def bounce_off_bottom(self, down_line):
        """
        line is a list object of a line ((x1, y1), (x2, y2))
        """
        y_down = down_line[0][1]
        if self.rect.bottom > down_line:
            self.v.y = -abs(self.v.y)  # turn speed up
            self.rect.bottom = y_down
        self.last_hline = down_line


class PlayerEntities(GravityEntities):
    def __init__(self, rect, img_dict):
        """
        pos, v, horspeed - lists
        """
        # constructor
        super().__init__(rect, img_dict)

        # horizontal speed
        #self.horspeed = horspeed
        self.jumpheight = -300  # jumpheight
        self.image = img_dict['idle'][0]

    def set_controls(self, controls):
        self.controls = controls  # the controls provided in the argument work



#class GameBorders:
#    def __init__(self):
#        """
#        Class for game borders for different rectangular levels
#        """
#        self.borders = {
#            'upside': (self.rect.topleft, self.rect.topright),
#            'rightside': (self.rect.topright, self.rect.bottomright),
#            'bottomside': (self.rect.bottomleft, self.rect.bottomright),
#            'leftside': (self.rect.topleft, self.rect.bottomleft)
#            }
#
#    def contains_sprite(self, sprite):
#        return self.rect.contains(sprite.rect)

# Todo
#class StaticObstacle(PhysicalObject):
#    def __init__(self, pos, v, horspeed, controls):
#        super().__init__(self, pic, dim)
#
#class StaticBonus(InteractiveObject):
#    def __init__(self, pos, v, horspeed, controls):
#        super().__init__(self, pic, dim)

#class LandscapeGroup(GameSpritesGroup):
#
#    def __init__(self, *sprites):
#        # constructor
#        super().__init__(self, *sprites)
#
#class ItemGroup(GameSpritesGroup):
#
#    def __init__(self, *sprites):
#        # constructor
#        super().__init__(self, *sprites)
#
#class PlayersGroup(GameSpritesGroup):
#
#    def __init__(self, *sprites):
#        # constructor
#        super().__init__(self, *sprites)
#
#class EnemiesGroup(GameSpritesGroup):
#
#    def __init__(self, *sprites):
#        # constructor
#        super().__init__(self, *sprites)


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
            'p1_run_right': ((1,0), 3),  # rect, image count
            'p2_run_right': ((1,3), 3)
    }
    images = {
            'p1_idle': [(0,0)],# list of tuples
            'p2_idle': [(0,3)]
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
    # Loading images from spritesheet
    ip = vi_.ImagePicker(filename, tile_size, gap, border, colorkey=True)
    ip.get_strips(image_rows)
    ip.get_images(images)
    ip.flip('p1_run_right','p1_run_left')
    ip.flip('p2_run_right','p2_run_left')
    # animations
    delay = 0.2
    animations_list = [
            'p1_run_right','p1_run_left','p2_run_right','p2_run_left'
            ]
    for animation in animations_list:
        ip.animate(animation, delay)
    ip.zoom_dict(2)
    new_images = ip.modified

    li = vi_.LevelImages(new_images, lvl_img, *ip.return_zoom_param())

    # Building level 0
    dim = (24,24)
    Level0 = l_.LevelData(dim, li)
    Level0.load_map(0)
    Level0.parse_map()
    world = World(Level0)
    world.add_players(['player1','player2'])

    # SpritesGroup setup
    all_sprites = GameSpritesGroup()
    player_dict = world.get_players()
    for key in player_dict:
        all_sprites.add_sprite(player_dict[key])


    # Game cycle
    while True:
        # handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # updating game
        time_passed = clock.tick(30)
        time_passed_seconds = time_passed / 1000.0


        # drawing all sprites
        all_sprites.update()
        changed_rects = all_sprites.draw(screen)
        pygame.display.update(changed_rects)
