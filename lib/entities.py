import pygame
import sys
import os
from lib import visual as vi_
from lib import vector as v_
from lib import spritesheetgaps as sp_
from lib import pyganim as anim_
from lib import levels as l_
from levels import levels as dicts_

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
    def __init__(self, rect, img_dict=None):
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
        self.rects = {}

        self.images = img_dict

    def move(self):
        pass

    def update(self):  # drawing method
        pass

    def set_sprite(self):
        pass

    def clear(self):
        self.image.fill(self.colorkey)

    def rects_from_sides(self, offset=2, out=False):
        d_offset = offset + offset
        top_l = self.rect.topleft  # topright point
        top_r = self.rect.topright  # topleft point
        bt_l = self.rect.bottomleft  # bottomright point
        width = self.rect.width  # width
        height = self.rect.height

        top_rect = [top_l[0]-offset, top_l[1]-offset, width+d_offset, d_offset]
        left_rect = [top_l[0]-offset, top_l[1]-offset, d_offset, height+d_offset]
        bottom_rect = [bt_l[0]-offset, bt_l[1]-offset, width+d_offset, d_offset]
        right_rect = [top_r[0]-offset, top_r[1]-offset, d_offset, height+d_offset]
        if out:  # if new rects should be strictly outside the old rect
            top_rect[1] -= offset
            left_rect[0] -= offset
            bottom_rect[1] += offset
            right_rect[0] += offset
        self.rects['top'] = pygame.Rect(top_rect)
        self.rects['left'] = pygame.Rect(left_rect)
        self.rects['bottom'] = pygame.Rect(bottom_rect)
        self.rects['right'] = pygame.Rect(right_rect)
        print(self.rects)

class GameBorders(GameObjects):
    def __init__(self, rect):
        """
        Class for game objects
        dim - (height, width)
        pic - Surface with image
        Objects' coordinates are initially (0,0)
        """
        super().__init__(rect)
        self.rects = {}
        self.rect = pygame.Rect(rect)

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

    def get_rect(self):
        return self.rect

    def update(self):
        pass


class FreeMovingEntities(GameEntities):
    def __init__(self, rect, img_dict):
        """
        Class for moving game objects that move freely
        Objects' coordinates are initially (0,0)
        """
        super().__init__(rect, img_dict)

        # attributes
        phys_dict = {
                'g': 300.0,
                'k': 50.0
                }
        self.pressing = {
                'right': False,
                'left':False
                }
        g = phys_dict['g']
        k = phys_dict['k']
        self.speed = v_.Vector2d((0,0))
        self.g_speed = v_.Vector2d((0,g))
        self.k = v_.Vector2d((k,0))
        self.falling = True
        self.rects_from_sides()

        # Attributes methods
    def get_mass(self):
        return self.mass

    def set_mass(self, new_mass):
        self.mass = new_mass

    def set_speed(self, new_speed):
        self.speed = new_speed

    def move(self, time):
        collision = self.check_collisions_with_borders()
        if collision is not None:
            if (collision == 1) or (collision == 2):
                self.pressing[collision] = False
            if (collision == 4):
                if (self.falling == True) and (self.speed.y > 0):
                    self.falling = False
        if self.falling:
            self.rect.centery += self.g_speed.y * time
        if self.speed.x is not 0:
            if self.speed.x > 0:
                self.speed.x -= self.k.x*time
            if self.speed.x < 0:
                self.speed.x += self.k.x*time
        self.rect.centerx += self.speed.x * time
        # update rects:
        self.rects['left'].center = self.rect.midleft
        self.rects['right'].center = self.rect.midright
        self.rects['top'].center = self.rect.midtop
        self.rects['bottom'].center = self.rect.midbottom
        print("Edited rects".format(self.rects))
        print("Is falling? - {}".format(self.falling))


    def set_colliding_list(self, border, *sprites_groups):
        """
        checks collisions with sprites in sprites groups
        """
        r_list = []
        b_list = []  # border list
        for s_group in sprites_groups:
            sprites = s_group.sprites()
            if self in sprites:  # checking and removing self from list
                sprites.remove(self)
            for sprite in sprites:
                rect = sprite.rect
                r_list.append(rect)
        self.r_list = r_list
        b_list.append(border)
        self.b_list = b_list

    def check_collisions_with_objects(self):
        collided = 0
        r_list = self.r_list
        # colliding with rects in list
        col_i = self.rect.collidelist(r_list)
        rect = r_list[col_i]
        if self.rects['left'].colliderect(rect):
            if self.rect.left < rect.right:
                if self.speed.x < 0:
                    self.speed.x = -self.speed.x
                self.rect.left = rect.right
                collided = 1
        elif self.rects['right'].colliderect(rect):
            if self.rect.right >= rect.left:
                self.rect.right = rect.left+1
                collided = 2
        if self.rects['bottom'].colliderect(rect):
            if self.rect.bottom > rect.top:
                if self.speed.y > 0:
                    self.speed.y = 0
                self.rect.bottom = rect.top
                collided = 4

        elif self.rects['top'].colliderect(rect):
            if self.rect.top < rect.bottom:
                if self.speed.y < 0:
                    self.speed.y = -self.speed.y
                self.rect.top = rect.bottom
                collided = 3
                print("collided {}".format(collided))
        return collided

    def check_collisions_with_borders(self):
        collided = 0
        b_list = self.b_list
        rect = b_list[0]
        print(b_list)
        # colliding with rects in list
        if self.rect.left <= rect.left:
            if self.speed.x < 0:
                self.speed.x = -self.speed.x
            self.rect.left += 15
            collided = 1
        if self.rect.right >= rect.right:
            if self.speed.x < 0:
                self.speed.x = -self.speed.x
            self.rect.right -= 15
            collided = 2
        if self.rect.bottom >= rect.bottom:
            if self.speed.y > 0:
                self.speed.y = 0
            self.rect.bottom -= 15
            collided = 4
        if self.rect.top <= rect.top:
            if self.speed.y < 0:
                self.speed.y = -self.speed.y
            self.rect.top += 15
            collided = 3
            print("collided {}".format(collided))
        return collided


class PlayerEntities(FreeMovingEntities):
    def __init__(self, rect, img_dict):
        """
        pos, v, horspeed - lists
        """
        # constructor
        super().__init__(rect, img_dict)
        phys_dict = {
                'horspeed': 5.0,
                'jumpheight': -100,
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
        self.horspeed = 200.0
        # horizontal speed
        self.jumpheight = -100  # jumpheight
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
            if not self.falling:
                self.speed.y = self.jumpheight
                self.states_dict['direction'] = 'center'
                self.falling = True
        if pressed[self.controls['down']]:
            self.speed.x = 0.0

    def update(self):

        # clean image
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
    img_path = '../images/spritesheet.png'
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, img_path)


    # Get images file and put name on images
    tile_size = (21,21)
    gap = 2
    border = 1
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
    image_rows = dicts_.get_dicts('rows')
    print(image_rows)
    images = dicts_.get_dicts('img')
    print(images)
    lvl_img = dicts_.get_dicts('lvl')

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
#    world.add_tiles(GameTiles, 'grass')

    # Adding objects not present in world:
    game_border = GameBorders((0,0,*resolution))

    # SpritesGroup setup
    player_sprites = GameSpritesGroup()
    player_dict = world.get_players()
    i = 0
    for key in player_dict:
        player=player_dict[key]
        player.set_mass(4)
        player.set_controls(controls[i])
        player.set_colliding_list(game_border.rect)
        player_sprites.add_sprite(player)
        i+=1

    all_sprites = GameSpritesGroup(player_sprites.sprites())

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
            player.move(time_passed_seconds)

        # drawing all sprites
        player_sprites.clear(screen, bg_image)
        player_sprites.update()
        print("Player1:{}".format(player_dict[0].rect))
        changed_rects = player_sprites.draw(screen)
        pygame.display.update()