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

# Color of the background
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


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        pygame.sprite.Sprite.__init__(self)  # launching init of the parent class
        self.image = pygame.Surface((50,100))  # create an attribute surface with fixed size
        self.image.fill((0, 0, 0))  # make the surface black
        self.rect = self.image.get_rect()  # make the attribute rect the same size as the image
        self.pos = pos  # vector of the position
        surface.blit(self.image, pos)  # draw the image on the argument surface
    

class Bonus:
    def __init__(self, pos, count = 1):
        self.image = pygame.Surface((15,15))  # create an attribute surface with fixed size
        self.image.fill(COLOR)  # fill the image with the background color --- background surface
        self.img = pygame.Surface((15,15))  # create an additional attribute surface with fixed size
        self.img.blit((self.image), (0,0))  # draw the img surface on the additional surface --- image surface
        self.pos = pos  # vector of the position
        self.count = count  # number of stars

    def collect(self, player):
        self.pos = (501, 501)  # position of the stars
        player.score += 500  # score
        self.image.fill(COLOR)  # fill the image with the background

    def update(self):
        self.image.fill(COLOR)  # fill the image with the background
        self.img = pygame.Surface((15,15))  # creating a new surface
        self.img.blit((self.image), (0,0))  # updating an image


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, v, horspeed, controls, color, anim_ar):
        pygame.sprite.Sprite.__init__(self)  # launching init of the parent class
        # 
        self.base = Vector(0.0, 1.0)  # base vector 
        self.pos = pos  
        self.v = v
        self.horspeed = horspeed
        self.baseline = 500.0 - 16.0       
        self.jumpheight = -300 
        self.controls = controls
        self.color = color
        self.movhor = 0
        self.score = 0.0
        #self.circle = Circle(20, self.pos)
        self.image = pygame.Surface((16, 16))
        self.image.fill(COLOR)
        self.state = ['ground', 'left']                
        self.image.set_colorkey(COLOR)
        self.rect = self.image.get_rect()
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
        screen.blit(self.image, (self.pos.x, self.pos.y))

class Box:

    def __init__(self, width = 500, height = 500, npoint = Vector(50.0, 100.0)):
       
        pygame.init()
        pygame.font.init()

        self.controlsP1 = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        self.controlsP2 = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]
        red = (204, 0, 0)
        blue = (0, 128, 255)
        self.green = (200, 255, 180)
        verdana = "/home/student/project2sem/Verdana.ttf"
        npoint2 = Vector(300, 100)
 #       obst= []
 #       for i in range (1, 8):
 #           obst[i] = (50 +50*i, 480-(30*i))
        #physics const
        self.k = 2.0
        self.g = 1000.0
        
        #player initialization
    
        basev = Vector(0.0, 0.0)
        basev2 = Vector(0.0, 0.0)
        first = Player(npoint, basev, 1000.0, self.controlsP1, blue, anim_p1)
        second = Player(npoint2, basev2, 1000.0, self.controlsP2, red, anim_p2)
        
        #screen
        self.num = 0
#        self.starlist = []
        size = width, height = 500, 500
        self.screen = pygame.display.set_mode(size)
        self.image = self.screen.copy()
        self.image.fill(COLOR)
        pygame.display.set_caption('Game')
        self.fix = self.screen.copy()
        self.fix.fill(COLOR)
        pygame.font.init()
        font = pygame.font.Font(None, 30)
        text = font.render("GAME", True, self.green)
        self.fix.blit(text, [230, 50])
        
       # for count in range(0, 50):
       #     star = Bonus((501, 501), count)
       #     self.starlist.append(star)
      #  ar = pygame.PixelArray(self.image)
  #      obst1 = Obstacle(obst[1], self.fix)
  #      obst2 = Obstacle(obst[2], self.fix)
  #     obst3 = Obstacle(obst[3], self.fix)
  #     obst4 = Obstacle(obst[4], self.fix)
  #     obst5 = Obstacle(obst[5], self.fix)
  #     obst6 = Obstacle(obst[6], self.fix)
  #     obst7 = Obstacle(obst[7], self.fix)
  #     obst8 = Obstacle(obst[8], self.fix)

        self.update(first, second)
        

    def update(self, player1, player2):
        a = Vector(501, 501)
        array = (501, 501)
        star = Bonus(a)
        clock = pygame.time.Clock()
        tt = 0
        while True:
            self.dt = clock.tick(50) /1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.type == pygame.MOUSEMOTION:
                        if event.buttons[0]:
                            pygame.draw.circle(self.fix, (0, 0, 0), event.pos, 20)
                        elif event.buttons[2]:
                            pygame.draw.circle(self.fix, COLOR, event.pos, 20)
                            if self.space:
                       # self.starlist[self.num].pos.x = pygame.MOUSEMOTION.pos[0]
                       # self.starlist[self.num].pos.y = pygame.MOUSEMOTION.pos[1]
                       # self.num += 1
                                array = event.pos
                                V = Vector(event.pos[0], event.pos[1])
                                star = Bonus(V)
                                self.space = 0

            tt += self.dt
            print("%f %f %f %f" % (tt, player1.v.x, player1.pos.x, player1.score))
            print("     %f %f %f %f" % (tt, player2.v.x, player2.pos.x, player2.score))
            pygame.font.init()
            font = pygame.font.Font(None, 30)
            score1 = font.render("Player 1 %f" %player1.score, True, self.green)
            score2 = font.render("Player 2 %f" %player2.score, True, self.green)
            self.fix.blit(score1, [0, 100])
            self.fix.blit(score2, [250, 100])

            self.image.fill((0, 25, 75))
            self.image.blit(self.fix, (0,0))
            #static graphics go here
            self.keyboard(player1)
            self.keyboard(player2)
            
            for j in range(0, self.num):
                if self.starlist[j].pos == player1.pos:
                    self.starlist[j].collect(player1)
                if self.star[j].pos == player2.pos:
                    self.starlist[j].collect(player2)

          #  pygame.sprite.collide_rect(player1, )
            player1.update(self.image, self.dt, self.g, self.k)
            player2.update(self.image, self.dt, self.g, self.k)
            self.image.blit(star.image, array)
            self.screen.blit(self.image, (0,0))
            pygame.display.flip()



    def keyboard(self, player1):
        pressed = pygame.key.get_pressed()
        if pressed[player1.controls[0]]:
            player1.state[1] = 'left'
            player1.v.x -= self.dt * player1.horspeed
        
        if pressed[player1.controls[1]]:
            player1.state[1] = 'right'
            player1.v.x += self.dt * player1.horspeed

        if pressed[player1.controls[2]]:
            if player1.pos.y == player1.baseline:
                player1.v.y = player1.jumpheight
                player1.state[0] = 'up'
            else:
                x = 1
        if pressed[player1.controls[3]]:
            player1.v.x = 0.0

        if pressed[pygame.K_SPACE]:
            self.space = 1

     #   if pressed[player2.controls[0]]:
      #      player2.side = 0
       #     player2.v.x -= self.dt * player2.horspeed

    #    if pressed[player2.controls[1]]:
    #        player2.side = 1
    #        player2.v.x += self.dt * player2.horspeed

    #    if pressed[player2.controls[2]]:
    #        if player2.pos.y == player2.baseline:
    #            player2.v.y = player2.jumpheight
    #        else:
    #            x = 1

world = Box()
