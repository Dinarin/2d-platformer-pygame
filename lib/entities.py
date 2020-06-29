import pygame
import sys
import os
from lib import visual as vi_
from lib import vector as v_
from lib import spritesheetgaps as sp_
from lib import pyganim as anim_
from lib import levels as l_
from lib import buttons as b_
from levels import tilesets as ts_
from pygame import freetype

# Events
# event1 = Event(type, **attributes)
class World:
    """Adds entities according to level data.
    """

    def __init__(self, level_data):
        """
        """

        # Preparing to track objects
        self.entities = {}
        self.tiles = []
        self.entity_id = 0
        self.tile_id = 0
        self.players = {}

        # List for text and buttons
        self.texts = []

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
    def add_tiles(self, tile_type, tile_name='snow'):
        """Adds tiles to the game
        """
        xys = self.obj_dict[tile_type]
        img_dict = self.imgs.get_obj(tile_type)
        # Stores the tile then advances the current id

        for xy in xys:
            rect = self.xy_to_rect(xy)
#            print("tile", rect, img_dict)
            self.tiles.append(GameTiles(rect, img_dict, tile_name))


    def add_players(self, player_images_list):
        i = 0
        for player_image_name in player_images_list:
            xy = self.obj_dict['player'][i]
            img_dict = self.imgs.get_obj(player_image_name)
            rect = self.xy_to_rect(xy)
            self.players[i] = PlayerEntities(rect, img_dict)
            i += 1

    def add_entities(self, EntityClass, entity_name):
        """Adds entities to the game
        """
        xys = self.obj_dict[entity_name]
        img_dict = self.imgs.get_obj(entity_name)
        # Stores the entity then advances the current id
        for xy in xys:
            rect = self.xy_to_rect(xy)
            self.entities[self.entity_id] = EntityClass(rect, img_dict, self.entity_id)
            self.entity_id += 1


    def add_text(self, TextClass, rect, font, color=None, size=14, align=0):
        self.texts.append(TextClass(rect, font, color, size, align))

    def get_tiles(self):
        return self.tiles

    def get_entities(self):
        return self.entities

    def get_players(self):
        return self.players

    def check_scores(self):
        """Checks scores of two players and returns the number of the winner.
        """
        player1 = self.players[0]
        player2 = self.players[1]

        if player1.score > player2.score:
            return 1
        elif player2.score > player1.score:
            return 2
        elif player2.score == player1.score:
            return 0



class GameObjects(pygame.sprite.DirtySprite):
    def __init__(self, rect, img_dict=None):
        """Class for all game objects.

            Args:
                rect (tup): (x, y, height, width)
                img_dict (dict): image dictionary with surfaces
        """
        super().__init__()

        # Setting DirtySprite attributes.
        self.dirty = 2
        self.visible = 1


        # Setting sprite attributes.
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
        """Method for creating pygame.Rect objects centered on each side.
            Args:
                offset (int): half of the shorter side of the new rectangle.
                out (bool): True if rectangles's area is strictly outside
                    the parent rectangle.
        """
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

class GameMenus(GameObjects):
    """Class for game menus.

        Arguments:
    """
    def __init__(self, rect, manager):
        super().__init__(rect)
        self.b_areas = []
        self.manager = manager

    def create_button_area(self, rect):
        b_area = b_.MenuButtons(rect, self.manager, self.image)
        self.b_areas.append(b_area)

    def debug(self):
        # blit menus on self.
        for b_area in self.b_areas:
            pygame.draw.rect(self.image, (255, 0, 0), b_area, 1)



class GameSpritesGroup(pygame.sprite.LayeredDirty):
    """Class for game sprite groups.
        Args:
            *sprites (:obj: pygame.sprite.Sprite): any number of sprite objects

    """
    def __init__(self, *sprites):
        # constructor
        super().__init__(*sprites)

    def update_objects(self):
        self.update(args)

    #?
    def add_sprite(self, sprite):
        self.add(sprite)

class GameFont(pygame.freetype.Font):
    def __init__(self, size=14):
        super().__init__(None, size)

    def write_with_font(self, text, fgcolor=None, size=14):
        return self.render(text, fgcolor=fgcolor, size=size)


class GameText(GameObjects):
    """Class for scoreboards and level data

        Args:
            game_font (:obj: GameFont)
    """
    def __init__(self, rect, game_font, color=None, size=14, align=0):
        super().__init__(rect)
        self.font = game_font
        self.left = 0
        self.right = 0
        self.size = size
        self.color = color
        self.set_alignment(align)
        self.text = None

    def set_text(self, text):
        """Writes the text string on the sprite.
            Args:
                text (str): string of text
        """
        self.image, self.rect = self.font.write_with_font(text, fgcolor=self.color, size=self.size)
        self.set_alignment(self.align)
        self.text = text

    def change_color(self, color):
        """Changes the font color of the sign.
            If there is already text in a different color, rewrites the text.

            Args:
                color (list): list of RGB values of a color.
        """
        if (self.color is not color) and (self.text is not None):
            self.image, self.rect = self.font.write_with_font(\
                self.text, fgcolor=self.color, size=self.size)
        self.color = color
        self.set_alignment(self.align)

    def set_alignment(self, align):
        """Sets alignment.
            align (int): number corresponding to alignment
                0 - no alignment
                1 - left
                2 - right
        """
        self.align = align
        if self.align == 1:
            self.rect.left = 8
        if self.align == 2:
            self.rect.right = 1000


#class Menu(pygame.Surface):
#    def __init__(self, dimensions):
#        super().__init__(self,)
#
#class ButtonGroup(GameSpritesGroup):
#    def __init__(self, *buttons):
#        super().__init__(self, *buttons)
#
#    def __





#class StaticText(GameText):
#
#class DynamicText
#
class GameBorders(GameObjects):
    def __init__(self, rect):
        """
        Class for game objects
        dim - (height, width)
        pic - Surface with image
        Objects' coordinates are initially (0,0)
        """
        super().__init__(rect)
        self.rects_from_sides(out=True)

class GameTiles(GameObjects):
    def __init__(self, rect, img_dict, tile_name, t_id=None):
        super().__init__(rect, img_dict)
        self.t_id = t_id
        self.image = img_dict[tile_name][0]

class GameEntities(GameObjects):
    def __init__(self, rect, img_dict, e_id=None):
        """
        Class for game objects
        dim - (height, width)
        pic - Surface with image
        id (int): entity_id
        Objects' coordinates are initially (0,0)
        """
        super().__init__(rect, img_dict)

        self.id = e_id

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
    def __init__(self, rect, img_dict, e_id=None):
        """
        Class for interactive game objects
        assumes that dimensions are the same is the picture
        Objects' coordinates are initially (0,0)
        """
        super().__init__(rect, img_dict, e_id)

    def get_rect(self):
        return self.rect

    def update(self):
        pass


class FreeMovingEntities(GameEntities):
    def __init__(self, rect, img_dict, e_id=None):
        """
        Class for moving game objects that move freely
        Objects' coordinates are initially (0,0)
        """
        super().__init__(rect, img_dict, e_id)

        # attributes
        phys_dict = {
                'g': 0.5,
                }
        self.pressing = {
                'right': False,
                'left':False
                }
        self.g = phys_dict['g']
        self.speed = v_.Vector2d((0,0))
        self.on_ground = False
        self.rects_from_sides()

        # Attributes methods

    def move(self):
        if not self.on_ground:
            self.speed.y += self.g
        self.on_ground = False
        self.rect.y += self.speed.y
        self.rects['top'].center = self.rect.midtop
        self.rects['bottom'].center = self.rect.midbottom

        self.check_y_collisions()

        self.rect.x += self.speed.x
        self.rects['left'].center = self.rect.midleft
        self.rects['right'].center = self.rect.midright

        self.check_x_collisions()


    def set_colliding_list(self, border, *sprites_groups):
        """
        checks collisions with sprites in sprites groups
        """
        r_list = []
        for s_group in sprites_groups:
            sprites = s_group.sprites()
            if self in sprites:  # checking and removing self from list
                sprites.remove(self)
            for sprite in sprites:
                rect = sprite.rect
                r_list.append(rect)
        r_list.extend(border.rects.values())
        self.r_list = r_list

    def check_x_collisions(self):
        collided = 0
        r_list = self.r_list
        # colliding with rects in list
        for rect in r_list:
            if self.rect.colliderect(rect):
                if self.speed.x < 0:
                    self.rect.left = rect.right
                    collided = 1
                if self.speed.x > 0:
                    self.rect.right = rect.left
                    collided = 2

    def check_y_collisions(self):
        collided = 0
        r_list = self.r_list
        # colliding with rects in list
        for rect in r_list:
            if self.rect.colliderect(rect):
                if self.speed.y > 0:
                    self.rect.bottom = rect.top
                    self.on_ground = True
                    self.speed.y = 0
                    collided = 4
                if self.speed.y < 0:
                    self.rect.top = rect.bottom
                    collided = 3
        return collided


class PlayerEntities(FreeMovingEntities):
    global_events = {
            'game': None
            }
    def __init__(self, rect, img_dict):
        """
        pos, v, horspeed - lists
        """
        # constructor
        super().__init__(rect, img_dict, e_id=None)
        phys_dict = {
                'horspeed': 7,
                'jumpheight': 10,
                }
        self.states = {
                'direction': 'left',
                'vertical': 'ground',
                }
        self.anim_dict = {
                ('left', 'ground'): 'run_left',
                ('right','ground'): 'run_right',
                ('left', 'jump'): 'jump_left',
                ('right', 'jump'): 'jump_right'
             }
        self.events = {
            'up': False,
                #                'down': False,
                'left': False,
                'right': False
                }

        self.last_state = None
        self.horspeed = phys_dict['horspeed']
        # horizontal speed
        self.jumpheight = phys_dict['jumpheight']  # jumpheight
        self.img_dict = img_dict
        self.current_animation = None
        self.score = 0

    def start_animation(self, animation_name):
        current_animation = self.img_dict[animation_name]
#        if current_animation == :
#            current_animation.nextFrame()
#        else:
        current_animation.play()
        self.current_animation = current_animation

    def set_controls(self, controls):
        self.controls = controls  # the controls provided in the argument work

    def get_keys(self, e):
        keys = self.controls
        if e.type == pygame.KEYDOWN and e.key == keys['up']:
            self.events['up'] = True
        if e.type == pygame.KEYDOWN and e.key == keys['left']:
            self.events['left'] = True
        if e.type == pygame.KEYDOWN and e.key == keys['right']:
            self.events['right'] = True

        if e.type == pygame.KEYUP and e.key == keys['up']:
            self.events['up'] = False
        if e.type == pygame.KEYUP and e.key == keys['left']:
            self.events['left'] = False
        if e.type == pygame.KEYUP and e.key == keys['right']:
            self.events['right'] = False

    def control(self):
        """Reads event dictionary and changes attributes.

        """
        controls = self.controls
        if self.events['left']:
            self.states['direction'] = 'left'
            self.speed.x = - self.horspeed

        if self.events['right']:
            self.states['direction'] = 'right'
            self.speed.x = self.horspeed

        if self.events['up']:
            if self.on_ground:
                self.states['direction'] = 'center'
                self.speed.y = -self.jumpheight
                self.states['vertical'] = 'jump'

        if not (self.events['left'] or self.events['right']):
            self.speed.x = 0

    def collect(self, sprites_group):
        """Bonus collection
        """
        for sprite in sprites_group.sprites():
            if sprite.active:
                if self.rect.collidepoint(sprite.rect.center):
                    sprite.dirty = 2
                    sprites_group.visible_count -= 1
                    sprite.visible = 0
                    self.score += 100
                    sprite.active = False
            if sprites_group.visible_count == 0:
                self.global_events['game'] = 'end'

    def update(self):
        self.control()
        self.move()

        # Changing states after moving.
        if (self.speed.x == 0) and (self.states['vertical'] == 'ground'):
            self.states['direction'] = 'center'
        if self.on_ground:
            self.states['vertical'] = 'ground'

        # Cleaning image and applying animations.
        self.clear()
        anim_tuple = (self.states['direction'],\
                self.states['vertical'])

        # Checking if the animation should change
        if (self.last_state != anim_tuple)\
                and (anim_tuple in self.anim_dict.keys()):
            self.start_animation(self.anim_dict[anim_tuple])
            self.last_state = anim_tuple

        # When the idle image should be shown.
        if (self.current_animation == None)\
                or (self.states['direction'] == 'center'):
            self.image.blit(self.img_dict['idle'][0], (0,0))
        else:
            self.current_animation.blit(self.image, (0,0))


# Todo
#class StaticObstacle(PhysicalObject):
#    def __init__(self, pos, v, horspeed, controls):
#        super().__init__(self, pic, dim)
#
class StaticBonus(GameEntities):
    bonus_list = [
            'star'
            ]
    def __init__(self, rect, img_dict, e_id=None):
        super().__init__(rect, img_dict, e_id)
        # pick first element from img dict
        self.image = img_dict[self.bonus_list[0]][0]
        self.active = True


class ItemGroup(GameSpritesGroup):

    def __init__(self, *sprites):
        # constructor
        super().__init__(self, *sprites)
        self.visible_count = len(self.sprites())

    def count_visible(self):
        self.visible_count = len(self.sprites())


if __name__ == "__main__":
    # Assigning necessary values to variables.
    # Setting number variables.
    resolution = (1008,1008)
    bg_color = (0,35,69)
    colorkey = (94,129,162)
    tile_dim = (21,21)
    map_dim = (24,24)  # level map dimensions
    gap = 2
    border = 2
    game_over = False

    # Setting string variables.
    bg_path = '../images/background.png'
    img_path = '../images/spritesheet_by_kenney_nl.png'

    # Finding full paths to image files no matter what folder we are in.
    dirname = os.path.dirname(__file__)
    bg_f_path = os.path.join(dirname, bg_path)
    img_f_path = os.path.join(dirname, img_path)

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

    # Loading tilesets dictionaries from file.
    images = ts_.get_dicts('img')
    image_rows = ts_.get_dicts('rows')
    lvl_img = ts_.get_dicts('level')


    # Pygame begins.
    # Opening pygame window and writing window name.
    pygame.freetype.init()
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption('Pygame platformer')

    # Loading background image and scaling it to resolution.
    bg_image_small = pygame.image.load(bg_f_path)
    bg_image = pygame.transform.scale(bg_image_small, resolution)
    screen.blit(bg_image, (0,0))

    # Creating pygame clock object.
    clock = pygame.time.Clock()


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
    world = World(Level)
    world.add_players(['player1','player2'])
    world.add_entities(StaticBonus, 'bonus')
    world.add_tiles('floating_tile', 'snow')
    world.add_tiles('ground_tile', 'snow')
    game_border = GameBorders((0,0,*resolution))


    # Adding objects to sprites groups.
    # Adding bonuses sprites to group.
    bonuses_dict = world.get_entities()
    bonuses_sprites = ItemGroup()
    for e_id in bonuses_dict:
        bonus = bonuses_dict[e_id]
        bonuses_sprites.add_sprite(bonus)
    # All bonuses sprites are in the group, can count how much there are.
    bonuses_sprites.count_visible()

    # Adding tiles sprites to group.
    tiles_list = world.get_tiles()
    tiles_sprites = GameSpritesGroup(*tiles_list)

    # Adding player sprites to group.
    # Player 1 has p_id = 0.
    # Player 2 has p_id = 1.
    player_dict = world.get_players()
    player_sprites = GameSpritesGroup()
    for p_id in player_dict:
        player=player_dict[p_id]
        player.set_controls(controls[p_id])
        player.set_colliding_list(game_border, tiles_sprites, player_sprites)
        player_sprites.add_sprite(player)

    # Adding text sprites.
    font = GameFont()
    text_color = ((30, 167, 255), (255, 204, 0))   # blue and yellow
    text_color2 = (232, 106, 23)  # red
    world.add_text(GameText, (500, 500, 2, 2), font, text_color[0], align=1)
    world.add_text(GameText, (500, 500, 2, 2), font, text_color[1], align=2)

    text_sprites = GameSpritesGroup(*world.texts)

    world.texts[0].set_text('Player 1: {}'.format(player_dict[0].score))

    world.texts[1].set_text('Player 2: {}'.format(player_dict[1].score))


    # Button test
    button = Button((100,100, 100,100))
    # Creating groups containing sprites from different groups.
    all_sprites = GameSpritesGroup(*text_sprites.sprites(), *player_sprites.sprites(), *tiles_sprites.sprites(), *bonuses_sprites.sprites(), button)
    non_player_sprites = GameSpritesGroup(*tiles_sprites.sprites(), *text_sprites.sprites(), *bonuses_sprites.sprites())


    # Game starts.
    while True:
        # Counting time between frames.
        time_passed = clock.tick(30)

        # Event handling.
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
            for p_id in player_dict:
                player = player_dict[p_id]
                player.get_keys(e)

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
                        world.add_text(GameText, (500, 500, 2, 2), font, text_color2, size=32)
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

        # Drawing all sprites on the display.
        # Clearing all sprites.
        all_sprites.clear(screen, bg_image)

        # Updating moving objects (only players).
        if not game_over:
            player_sprites.update()

        # Drawing all sprites.
        changed_rects = all_sprites.draw(screen, bg_image)

        # Updating the display.
        pygame.display.update()

