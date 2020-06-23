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
        self.rect = pygame.Rect(rect)
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.colorkey = (94,129,162)
        self.image.fill(self.colorkey)
        self.image.set_colorkey(self.colorkey)

        self.images = img_dict

    def move(self):
        pass

    def update(self):  # drawing method
        pass

    def set_sprite(self):
        pass

    def clear(self):
        self.image.fill(self.colorkey)

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
        phys_dict = {
                'k': 2.0,
                'g': 1000.0
                }
        g = phys_dict['g']
        self.gravity = True
        self.last_hline = None  # attribute that stores horizontal line
        self.speed = v_.Vector2d((0,0))
        self.g_acceleration = v_.Vector2d((0,g))
        self.k = phys_dict['k']

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
        y_line = 1008
        x1 = self.last_hline[0][0]
        x2 = self.last_hline[1][0]
        if (self.rect.bottom == y_line) and self.is_in_between_x(x1, x2):
            return True
        else:
            return False


    def fall(self, time):
        if self.rect.bottom is not 1008:
            gt = self.g_acceleration * time
        else:
            gt = v_.Vector2d((0.0,0.0))
        self.speed.x -= time * self.speed.x * self.k
        self.speed.y -= time * self.speed.y * self.k - gt.y
        self.rect.centerx += self.speed.x * time
        self.rect.centery += self.speed.y * time


    def update(self, time):
        self.gravity(time)

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
        phys_dict = {
                'horspeed': 500.0,
                'jumpheight': -300,
                'movhor': 0.0
                }
        self.states_dict = {
                'direction': 'left',
                'vertical': 'ground',
                }
        self.anim_dict = {
                ('left', 'ground'): 'run_left',
                ('right','ground'): 'run_right'
             }
        self.last_state = None
        horspeed = 1000.0
        # horizontal speed
        self.horspeed = horspeed
        self.jumpheight = -300  # jumpheight
        self.img_dict = img_dict
        self.current_animation = None

    def start_animation(self, animation_name):
        current_animation = self.img_dict[animation_name]
        current_animation.play()
        self.current_animation = current_animation

    def set_controls(self, controls):
        self.controls = controls  # the controls provided in the argument work

    def control(self, pressed, time):
        controls = self.controls
        if pressed[self.controls['left']]:
            self.states_dict['direction'] = 'left'
            self.speed.x -= time * self.horspeed

        if pressed[self.controls['right']]:
            self.states_dict['direction'] = 'right'
            self.speed.x += time * self.horspeed

        if pressed[self.controls['up']]:
            #   if self.rect.bottom == self.baseline:
            self.speed.y = self.jumpheight
            self.states_dict['direction'] = 'center'
        if pressed[self.controls['down']]:
            self.speed.x = 0.0
          #  if pressed[pygame.K_SPACE]:
          #      self.space = 1

    def update(self):
        self.clear()
        anim_tuple = (self.states_dict['direction'],\
                self.states_dict['vertical'])
        if ((self.last_state is not anim_tuple) and (anim_tuple in self.anim_dict.keys())):
            self.start_animation(self.anim_dict[anim_tuple])
            self.last_state = anim_tuple
        if self.current_animation == None:
            self.image.blit(self.img_dict['idle'][0], (0,0))
        else:
            self.current_animation.blit(self.image, (0,0))



class GameBorders:
    def __init__(self):
        """
        Class for game borders for different rectangular levels
        """
        self.borders = {
            'upside': (self.rect.topleft, self.rect.topright),
            'rightside': (self.rect.topright, self.rect.bottomright),
            'bottomside': (self.rect.bottomleft, self.rect.bottomright),
            'leftside': (self.rect.topleft, self.rect.bottomleft)
            }

    def contains_sprite(self, sprite):
        return self.rect.contains(sprite.rect)

# Todo
#class StaticObstacle(PhysicalObject):
#    def __init__(self, pos, v, horspeed, controls):
#        super().__init__(self, pic, dim)
#
#class StaticBonus(GameEntity):
#    def __init__(self, rect, img_dict):
#        super().__init__(self, rect, img_dict)

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
    img_path = '../images/small_spritesheet_by_kenney_nl.png'
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
    world = World(Level0)
    world.add_players(['player1','player2'])

    # SpritesGroup setup
    all_sprites = GameSpritesGroup()
    player_dict = world.get_players()
    i = 0
    for key in player_dict:
        player=player_dict[key]
        player.set_mass(4)
        player.set_controls(controls[i])
        all_sprites.add_sprite(player)
        i+=1


    # Game cycle
    while True:
        # updating game
        time_passed = clock.tick(30)
        time_passed_seconds = time_passed / 1000.0

        # handling events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pressed = pygame.key.get_pressed()
        for key in player_dict:
            player=player_dict[key]
            player.control(pressed, time_passed_seconds)
            player.fall(time_passed_seconds)

        # drawing all sprites
        all_sprites.clear(screen, bg_image)
        all_sprites.update()
        changed_rects = all_sprites.draw(screen)
        pygame.display.update()
