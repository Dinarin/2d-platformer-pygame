import sys, pygame
import math
import lib.objects as objects
import lib.canvas as canvas

# Initializing pygame
pygame.init()

# Temporary variables
window_size = (800,600)
canvas_size = (10,10)

# Creating the main surface
game_screen = pygame.display.set_mode(window_size)

# Creating canvas
canvas = canvas.Canvas(canvas_size)

# Game cycle
clock = pygame.time.Clock()
tt = 0
while True:
    dt = clock.tick(50) /1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    tt += dt
    game_screen.blit(a, (400,400))
    pygame.display.flip()
