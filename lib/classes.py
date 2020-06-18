import pygame
import sys
import pygame.sprite
import vector

# Events
# event1 = Event(type, **attributes)
class Level:
    """
    Stores level data
    """

    def __init__(self, player_image, background_image):
        self.player = player_sprite


class MainGame:
    def __init__(self, resolution):

        # initializing pygame
        pygame.init()

        # opening window
        self.screen = pygame.display.set_mode(resolution)
        self.state = 'running'
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('Game')

    def start_game(self):
        # variables
        # Temporary variables
        window_size = (1024,768)
        canvas_size = (800,600)
        circle_coords = (350,250)
        canvas_topleft = (112, 84)
        circle_dimensions = (42, 42)
        blue = (230, 255, 247)

        main_dict = {
#                'background': '',
            'player': {

    }
                }

        # Background
        bg_image = pygame.Surface(canvas_size)
        bg_image.fill((163,242,211))
        phys_dict = {
                'g': 1000.0,
                'k': 2.0
                }

        # Creating game objects
        camera = GameView(canvas_topleft, canvas_size, bg_image)  # gameview
        activity = GameActivity(sprites_dict, phys_dict)

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


            # drawing screen
            camera.find_render_group()
            changed_rects = camera.render()
            pygame.display.update(changed_rects)


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

    def find_render_group(self, activity):
        self.render_group = activity.get_render_group


class GameActivity:
    def __init__(self, sprites_dict, variables_dict):  # some sort of stored level data should be the arguments
        player_sprite = sprites_dict['player']
        player1 = PlayerObject(player_sprite, )
        self.render_g = GameSpritesGroup(player1)

    def get_render_group(self):
        return self.render_g


class GameSpritesGroup(pygame.sprite.RenderUpdates):

    def __init__(self, *sprites):
        # constructor
        super().__init__(self, *sprites)

    def update_objects(self):
        self.update(args)

    #?
    def add_sprite(self, sprite):
        self.add(sprite)


class GameObject(pygame.sprite.DirtySprite):
    def __init__(self, pic, dim):
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
        self.image = pic
        self.rect = Rect((0,0), dim)

    def move(self):
        pass
    def update(self):  # drawing method
        pass


class InteractiveObject(GameObject):
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

class MovingObject(GameObject):
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


class GravityObject(MovingObject):
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

    def move(self):
        if self.is_on_floor == False:
            self.speed += (g_acceleration * (1/self.mass)) * delta_t
            self.rect.y += self.speed.y * delta_t
        else:
            self.acceleration = 0.0
            self.v.y = 0.0
        self.v.x -= delta * self.v.x * k
        self.v.y -= delta * self.v.y * k - gt
        self.rect.centerx += self.v.x * delta
        self.rect.centery += self.v.y * delta


#    def update(self, delta, g, k):

class PhysicalObject(InteractiveObject):
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


class PlayerObject(GravityObject, PhysicalObject):
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



class GameBorder(InteractiveObject):
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
    resolution = (1024,768)
    game = MainGame(resolution)
    game.start_game()
