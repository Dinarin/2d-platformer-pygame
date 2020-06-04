import sys, pygame
import math
import lib.objects as objects
import lib.canvas as canvas

# Initializing pygame
pygame.init()

# Temporary variables
window_size = (1024,768)
canvas_size = (800,600)
circle_coords = (350,250)
canvas_topleft = (112, 84)
circle_dimensions = (100, 100)
blue = (0,0,255)

# Creating the main surface
game_screen = pygame.display.set_mode(window_size)

# Creating background
background = pygame.Surface(canvas_size)
background.fill(blue)

# Creating canvas
canvas_screen = canvas.Canvas(canvas_size, background)


# Creating an object
rect_obj = objects.RectObject(circle_coords, circle_dimensions)
# Creating sprite object
circle = canvas.ObjectSurface(circle_dimensions)
# Game cycle
clock = pygame.time.Clock()
tt = 0
gravity = objects.Vector(0,20)
while True:
    dt = clock.tick(1)/10

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    tt += dt
    canvas_screen.draw_object(rect_obj, circle)
    game_screen.blit(canvas_screen, canvas_topleft)
    pygame.display.flip()
    rect_obj.move_self(gravity)
