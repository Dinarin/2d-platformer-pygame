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
circle_dimensions = (42, 42)
blue = (230, 255, 247)

fps = 30
dt = 1.0/fps
accumulator = 0
g = objects.Vector(0,0.1)

def update_game_physics(delta_t, g_acceleration, obj_list):
    # game object behaviour
#    print(canvas_screen.rect.y < circle_obj.rect.y)
#    print(circle_obj)
#    print(circle_obj.rect.bottom, canvas_screen.rect.bottom)
#    if (circle_obj.rect.bottom < canvas_screen.rect.bottom) and not on_floor:
    for obj in obj_list: 
        obj.update_obj_physics(delta_t, g_acceleration)



# Keyboard
#borders_list = [(
#    canvas_size
# Creating the main surface
game_screen = pygame.display.set_mode(window_size)
on_floor = 0

# Creating background
background = pygame.Surface(canvas_size)
background.fill(blue)

# Creating canvas
canvas_screen = canvas.Canvas(canvas_topleft, canvas_size, background)

# Listing borders
borders = [
        (canvas_screen.rect.topleft,canvas_screen.rect.bottomleft),
        (canvas_screen.rect.bottomleft,canvas_screen.rect.bottomright),
        (canvas_screen.rect.bottomright,canvas_screen.rect.topright),
        (canvas_screen.rect.topright,canvas_screen.rect.topleft)
        ]
print(borders)


# Creating an object
circle_obj = objects.GameObject(circle_coords, circle_dimensions)
list_obj = [circle_obj]
circle_obj.set_circle_sprite()

# Game cycle
clock = pygame.time.Clock()
tt = 0

# gravity
jump = objects.Vector(0,-10)
pygame.draw.line(canvas_screen, (0,255,0), borders[1][0], borders[1][1])
while True:
    # Each cycle is drawing one frame

    # Time cycle and events
    accumulator += clock.tick(30)
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
            circle_obj.add_momentum(jump)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    while (accumulator > dt):
        update_game_physics(dt, g, list_obj)
        accumulator -= dt

    # Rendering game
    # updating object attributes before drawing
    circle_obj.update_state()

    # drawing object
    canvas_screen.draw_object(circle_obj)
    game_screen.blit(canvas_screen, canvas_topleft)
    pygame.draw.line(game_screen, (0,255,0), borders[1][0], borders[1][1], 10) 
    pygame.display.flip()

