import sys
import pygame
import math
import pyganim
import numpy as num
# Animations

anim_delay = 0.2
anim_r = [('pixels/player1.png'),
        ('pixels/player2.png'),
        ('pixels/player3.png')]
anim_l = [('pixels/player1l.png'),
        ('pixels/player2l.png'),
        ('pixels/player3l.png')]
anim_jump_l = [('pixels/playerjl.png', 0.2)]
anim_jump_r = [('pixels/playerj.png', 0.2)]
anim_idle = [('pixels/player0.png', 0.2)]


anim_r2 = [('pixels/player1a.png'),
        ('pixels/player2a.png'),
        ('pixels/player3a.png')]
anim_l2 = [('pixels/player1la.png'),
        ('pixels/player2la.png'),
        ('pixels/player3la.png')]
anim_jump_l2 = [('pixels/playerjla.png', 0.2)]
anim_jump_r2 = [('pixels/playerja.png', 0.2)]
anim_idle2 = [('pixels/player0a.png', 0.2)]

starim = 'pixels/star.png'  # Image for star

# Lists with animated pictures
anim_p1 = [anim_r, anim_l, anim_jump_l, anim_jump_r, anim_idle]
anim_p2 = [anim_r2, anim_l2, anim_jump_l2, anim_jump_r2, anim_idle2]

# Switching game modes
mode = ('editor', 'play')
modesw = mode[0]

# Global variables (temporary)
player_sprite_size = (16,16)


COLOR = (200, 200, 200)




# Declaring classes
class Vector:
    def __init__(self, x = 0.0, y = 0.0):
        sqrt = (x*x+y*y)**0.5
        self.length = sqrt
        self.x = x
        self.y = y

    def __add__(self, v1):
        self.x += v1.x
        self.y += v1.y

    def __sub__(self, v1):
        self.x -= v1.x
        self.y -= v1.y

    def normcord(self):
        self.nx = self.x/self.length
        self.ny = self.y/self.length

    def __mul__(self, a):
        self.x = self.x * a
        self.y = self.y * a

    def dot(self, a):
        self.dot1 = self.x * a.x + self.y * a.y

class PlayerObjects:
    def __init__(self, pos, v, horspeed, controls):
        # Setting attribute
        self.rect = pygame.Rect()
        self.rect.center = pos
        self.base = Vector(0.0, 1.0)  # base vector
        self.v = v  # speed
        self.horspeed = horspeed  # horizontal speed
        self.baseline = 500.0 - 16.0  # where is the floor
        self.jumpheight = -300  # jumpheight
        self.controls = controls  # the controls provided in the argument work
        self.movhor = 0  # ?
        self.state = ['ground', 'left']
        # Score from bonuses
        self.score = 0.0

    def update(self, screen, delta, g,k):
        #  if self.side:
        if self.pos.y <= self.baseline:
            gt = g*delta
        else:
            gt = 0.0
            self.v.y = 0.0
        self.v.x -= delta * self.v.x * k
        self.v.y -= delta * self.v.y * k - gt
        self.pos.x += self.v.x * delta
        self.pos.y += self.v.y * delta

        if self.pos.x < 16:
            if self.v.x < 0:
                self.v.x = -self.v.x
            self.pos.x = 16.0
        if self.pos.y < 16:
            if self.v.y < 0:
                self.v.y = -self.v.y
            self.pos.y = 16.0
        if self.pos.x > 484:
            if self.v.x > 0:
                self.v.x = -self.v.x
            self.pos.x = 484
        if self.pos.y > 484:
            if self.v.y > 0:
                self.v.y = 0
            self.pos.y = 484

# Graphical part of game objects
class GameSprites(pygame.sprite.Sprite):
    def __init__(self, obj):
        pygame.sprite.Sprite.__init__(self)
        self.rect = obj.rect
        self.image = pygame.Surface((obj.w, obj.h))  # create an attribute surface with fixed size
#        self.rect = self.image.get_rect()  # make the attribute rect the same size as the image
#        self.rect.topleft = pos

class Obstacle(GameSprites):
    def __init__(self, pos, obj_size):
        GameSprites.__init__(self, obj)
        self.image.fill((0, 0, 0))  # make the surface black
#        surface.blit(self.image, pos)  # draw the image on the argument surface

# Doesn't work
class Bonus(GameSprites):
    def __init__(self, obj, count = 1):
        GameSprites.__init__(self, obj)
        self.image = pygame.Surface((15,15))  # create an attribute surface with fixed size
#        self.image.fill(COLOR)  # fill the image with the background color --- background surface
#        self.img = pygame.Surface((15,15))  # create an additional attribute surface with fixed size
#        self.img.blit((self.image), (0,0))  # draw the img surface on the additional surface --- image surface
        self.count = count  # number of stars


# Moving part of game objects
class MovingSprites(GameSprites):
    moving_sprites = pygame.sprite.Group()
    def __init__(self, obj):
        GameSprites.__init__(self, obj)
        moving_sprites.add(self.sprite)  # easily redrawing
    def draw(self, surface, background):
        moving_sprites.clear(surface, background)
        moving_sprites.draw(surface)

    def collect(self, player):
        self.pos = (501, 501)  # position of the stars
        player.score += 500  # score
#        self.image.fill(COLOR)  # fill the image with the background

    def update(self):
        pass
#        self.image.fill(COLOR)  # fill the image with the background
#        self.img = pygame.Surface((15,15))  # creating a new surface
#        self.img.blit((self.image), (0,0))  # updating an image


# Class describing player sprite
class PlayerSprites(MovingSprites):
    def __init__(self, player_obj, anim_ar):
        MovingSprites.__init__(self, player_obj)
        boltAnim = []
        for anim in anim_ar[0]:
            boltAnim.append((anim, anim_delay))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        boltAnim = []
        for anim in anim_ar[1]:
            boltAnim.append((anim, anim_delay))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()
        boltAnim = []
        self.boltAnimStay = pyganim.PygAnimation(anim_ar[4])
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))
        self.boltAnimJumpLeft= pyganim.PygAnimation(anim_ar[2])
        self.boltAnimJumpLeft.play()
        self.boltAnimJumpRight= pyganim.PygAnimation(anim_ar[3])
        self.boltAnimJumpRight.play()


        self.draw(screen)

    def draw(self, screen):
        if self.state[1] == 'left':
            self.image.fill(COLOR)
            if self.state[0] == 'up':
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))

        if self.state[1] == 'right':
            self.image.fill(COLOR)
            if self.state[0] == 'up':
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))
        if self.pos.y == self.baseline:
            self.v.dot(self.base)
            if self.v.dot1 <= 0.0:
                self.state[0] = 'ground'
                if self.v.x == 0:
                    self.image.fill(COLOR)
                    self.boltAnimStay.blit(self.image, (0, 0))
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Main window class
class Box:
    def __init__(self, player_array, width = 500, height = 500, npoint = Vector(50.0, 100.0)):
        pygame.init()
        pygame.font.init()
        # controls for players
        self.controlsP1 = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        self.controlsP2 = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]
        # colors
        red = (204, 0, 0)
        blue = (0, 128, 255)
        self.green = (200, 255, 180)
        verdana = "/home/student/project2sem/Verdana.ttf"
        npoint2 = Vector(300, 100)
        #obst= []
        #for i in range (1, 8):
        #    obst[i] = (50 +50*i, 480-(30*i))

        #player initialization

        basev = Vector(0.0, 0.0)
        basev2 = Vector(0.0, 0.0)

        # dictionary with players data
        players_dict = {
                'player_obj': [PlayerObj(npoint, basev, g, controlsP1, player_obj_size, anim_p1), PlayerObj(npoint2, basev2, g, controlsP2, player_obj_size, anim_p2)],
                'anim_p': [anim_p1, anim_p2]
                }

        # list with player sprites, not moving sprites and moving sprites
        sprites_list = [PlayerSprites(players_dict['player_obj'][i], players_dict['anim_p'][i])  for i in range(2) ] + static_sprites_list + moving_sprites.sprites()
        #screen
        self.num = 0
        #self.starlist = []
        size = width, height = 500, 500
        self.screen = pygame.display.set_mode(size)
        self.image = self.screen.copy()
        self.image.fill(COLOR)
        pygame.display.set_caption('Game')
        pygame.font.init()
        font = pygame.font.Font(None, 30)
        text = font.render("GAME", True, self.green)
        self.image.blit(text, [230, 50])

        # for count in range(0, 50):
        #     star = Bonus((501, 501), count)
        #     self.starlist.append(star)
        # ar = pygame.PixelArray(self.image)
        # obst1 = Obstacle(obst[1], self.fix)
        # obst2 = Obstacle(obst[2], self.fix)
        # obst3 = Obstacle(obst[3], self.fix)
        # obst4 = Obstacle(obst[4], self.fix)
        # obst5 = Obstacle(obst[5], self.fix)
        # obst6 = Obstacle(obst[6], self.fix)
        # obst7 = Obstacle(obst[7], self.fix)
        # obst8 = Obstacle(obst[8], self.fix)

        # updating

    def update(self, obj_list):

            print("%f %f %f %f" % (tt, player1.v.x, player1.pos.x, player1.score))
            print("     %f %f %f %f" % (tt, player2.v.x, player2.pos.x, player2.score))

            # Interface
            pygame.font.init()
            font = pygame.font.Font(None, 30)
            score1 = font.render("Player 1 %f" %player1.score, True, self.green)
            score2 = font.render("Player 2 %f" %player2.score, True, self.green)
            self.image.blit(score1, [0, 100])
            self.image.blit(score2, [250, 100])

            self.screen.fill((0, 25, 75))
            self.screen.blit(self.fix, (0,0))




    def draw(self, sprite_list):
            # Updating players
            for sprite in sprite_list:
                sprite.draw(self.screen)
            pygame.display.flip()


# Keyboard method
def keyboard_players(player):
    pressed = pygame.key.get_pressed()
    if pressed[player.controls[0]]:
        player.state[1] = 'left'
        player.v.x -= self.dt * player.horspeed

    if pressed[player.controls[1]]:
        player.state[1] = 'right'
        player.v.x += self.dt * player.horspeed

    if pressed[player.controls[2]]:
        if player.pos.y == player.baseline:
            player.v.y = player.jumpheight
            player.state[0] = 'up'
        else:
            x = 1
    if pressed[player.controls[3]]:
        player.v.x = 0.0

        if pressed[pygame.K_SPACE]:
            self.space = 1

#physics const
k = 2.0
g = 1000.0
a = Vector(501, 501)
array = (501, 501)
star = Bonus(a)
clock = pygame.time.Clock()
tt = 0
while True:
    dt = clock.tick(50) /1000.0
    tt += dt
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:
                    pygame.draw.circle(self.image, (0, 0, 0), event.pos, 20)
                elif event.buttons[2]:
                    pygame.draw.circle(self.image, COLOR, event.pos, 20)
#                    if self.space:
#                        array = event.pos
#                        V = Vector(event.pos[0], event.pos[1])
#                        star = Bonus(V)
#                        self.space = 0

# Storing keyboards

player1.update(dt, g, k)
player2.update(dt, g, k)

world = Box()
Box.update(player1, player2)
