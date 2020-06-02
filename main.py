import sys, pygame
import math

pygame.init()

# Variables
size = width, height = 500, 500
speed = [2, 2]
a = 500.0
k = 2.0
x, y = 100, 100
vx, vy = 0, 0
g = 50.0
s = 50.0
clock = pygame.time.Clock()
earth = 0
baseline = 480.0

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Game')
prev_t = pygame.time.get_ticks()
tt = 0
ar = pygame.PixelArray(screen)
while True:
  delta = clock.tick(50) / 1000.0
  for event in pygame.event.get():
    if event.type == pygame.QUIT: sys.exit()
  tt += delta
  print( "%f %f %f" % (tt, vx, x))
  pressed = pygame.key.get_pressed()
  if pressed[pygame.K_LEFT]:
    vx -= delta * a
  if pressed[pygame.K_RIGHT]:
    vx += delta * a
  if pressed[pygame.K_UP]:
    if y == baseline:
      vy = -700.0
    else:
      earth = 0

  if y <= baseline:
    gt = 1000*delta
  else:
    gt = 0.0
    vy = 0.0
  vx -= delta * vx * k
  vy -= delta * vy * k - gt
  x += vx * delta
  y += vy * delta

  if x < 20:
    if vx < 0:
      vx = -vx
    x = 20
  if y < 20:
    if vy < 0:
      vy = -vy
    y = 20
  if x > 480:
    if vx > 0:
      vx = -vx
    x = 480
  if y > 480:
    if vy > 0:
      vy = 0
    y = 480
  
  aplatf = [150, 450, 50, 20]

  uy = y-20.0
  by = y+20.0

  rx = x+20.0
  lx = x-20.0

  if (by == 390.0) & (lx >= 100.0) & (rx <=200):
    vy = 1000*delta
    y = 370.0
    baseline = 370.0
  else:
    baseline = 480.0
  if rx == 100.0:
    if vx > 0.0: vx = -vx
    x = 80.0
  if uy == 430.0:
    if vy < 0.0:
      vy = -vy
    y = 450.0
  if lx == 200.0:
    if vx < 0.0:
      vx = -vx
    x = 220.0
  screen.fill((0, 25, 75))
  col = min(255, int(math.sqrt(vx ** 2 + vy ** 2)) + 100)
  pygame.draw.lines(screen, (255, 0, 0), True, [(100,390),(100,430),(200,430),(200,390)], 2)
 
  pygame.draw.circle(screen, (col-100, col-25, col), (int(x), int(y)), 20)        
  pygame.display.flip()

