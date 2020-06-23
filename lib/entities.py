import pygame
import sys
import os
from lib import visual as vi_
from lib import vector as v_
from lib import spritesheetgaps as sp_
from lib import pyganim as anim_

# Events
# event1 = Event(type, **attributes)
class LevelManager:
    """
    Stores level data
    """

    def __init__(self, spritefile):
        self.entities = {}
        self.entity_id = 0

    # Managing entities
    def add_entity(self, entity):

        # Stores the entity then advances the current id
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def remove_entity(self, entity):
        del self.entities[entity.id]

    def get(self, entity_id):

        # Find the entity, given its id (or None if it is not found)
        if entity_id in self.entities:
            return self.entitites[entity_id]
        else:
            return None

    # Managing sprites
    def set_player_sprite(self, rect, colorkey = None):
        self.player = self.sprites.image_at(rect, colorkey)

    def get_player_sprite(self):
        return self.player


    def load_map_data(..):
        char c
        int currentIndex = -1


class LevelData:
    """
    Stores level data
    """

    def __init__(self, spritefile):
        self.entities = {}
        self.entity_id = 0
        self.tiles_list = []

    # Managing entities
    def add_entity(self, entity):

        # Stores the entity then advances the current id
        self.entities[self.entity_id] = entity
        entity.id = self.entity_id
        self.entity_id += 1

    def remove_entity(self, entity):

        del self.entities[entity.id]

    def get(self, entity_id):

        # Find the entity, given its id (or None if it is not found)
        if entity_id in self.entities:
            return self.entitites[entity_id]
        else:
            return None

    # Managing sprites
    def set_player_sprite(self, rect, colorkey = None):
        self.player = self.sprites.image_at(rect, colorkey)

    def get_player_sprite(self):
        return self.player

class LevelBasic(LevelData):
    """
    Class for basic levels. All tiles used are stored as a class variable
    """
    def __init__(self):
        self.dim = (12, 24)
        self.tiles = []

    def add_line(self, string):
        """
        Method used in parsing a level file
        """
        half_len = self.dim[0]
        height = self.dim[1]
        if (len(self.tiles) < height):  # checking if the level is full
            if (len(string) == half_len):
                lvl_str = string + string[::-1]
                self.tiles.append(lvl_str)
            else:
                raise ValueError("Level string is not the right length")
        else:
            raise Exception("Level is full")

class GameSpritesGroup(pygame.sprite.RenderUpdates):

    def __init__(self, *sprites):
        # constructor
        super().__init__(self, *sprites)

    def update_objects(self):
        self.update(args)

    #?
    def add_sprite(self, sprite):
        self.add(sprite)


class GameEntity(pygame.sprite.DirtySprite):
    def __init__(self, img_dict, dim):
        """
        Class for game objects
        dim - (height, width)
        pic - Surface with image
        Objects' coordinates are initially (0,0)
        """
        super().__init__(self)

        #DirtySprite attributes
        self.dirty = False
        self.visible = True

        # Setting game object attributes
        #self._quality = object_dict['quality']

        # Setting sprite attributes
        self.image = None
        self.rect = Rect((0,0), dim)
        self.images = img_dict

    def move(self):
        pass

    def update(self):  # drawing method
        pass

    def set_sprite(self):
        pass

class InteractiveEntity(GameEntity):
    def __init__(self, pic, dim):
        """
        Class for interactive game objects
        assumes that dimensions are the same is the picture
        Objects' coordinates are initially (0,0)
        """
        super().__init__(self, pic, dim)

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

class MovingEntity(GameEntity):
    def __init__(self, pic, dim):
        """
        Class for moving game objects
        Objects' coordinates are initially (0,0)
        """
        super().__init__(self, pic, dim)

    def set_speed(self, new_speed):
        self.speed = new_speed

    def move(self):
        pass

    def update(self):
        pass


class GravityEntity(MovingEntity):
    def __init__(self, pic, dim):
        """
        Class for moving game objects that obey gravity
        Objects' coordinates are initially (0,0)
        """
        super().__init__(self, pic, dim)

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

class PhysicalEntity(InteractiveEntity):
    def __init__(self, pic, dim):
        """
        Class for game objects that have impassable borders
        assumes that dimensions are the same is the picture
        Objects' coordinates are initially (0,0)
        """
        super().__init__(self, pic, dim)

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


class PlayerEntity(GravityEntity, PhysicalEntity):
    def __init__(self, pic, dim, controls):
        """
        pos, v, horspeed - lists
        """
        # constructor
        super().__init__(self, pic, dim)

        # horizontal speed
        self.horspeed = horspeed
        self.jumpheight = -300  # jumpheight
        self.controls = controls  # the controls provided in the argument work



class GameBorder(InteractiveEntity):
    def __init__(self, pic, dim):
        """
        Class for game borders for different rectangular levels
        """
        super().__init__(self, pic, dim)
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
    sprites_path = '../pixels/small_spritesheet_by_kenney_nl.png'
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, sprites_path)


    # Get sprites file and put name on sprites

    sprite_rows = {
            'player1': ((0,0,21,21), 5, 2),  # rect, image count, gap in pixels
            'player2': ((0,69,21,21), 5, 2)
    }
    sp = vi.SpriteSheet(filename, colorkey=True)
    sp.get_strips(sprite_rows)
    sp.zoom(3)
    print(sp.sprites)
    new_sprites = sp.modified
    print(new_sprites)
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
        for key in new_sprites:
            for sprite in new_sprites[key]:
                screen.blit(sprite, (500,500))
                pygame.time.wait(1000)
                pygame.display.update()

        pygame.display.update()

