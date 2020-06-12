import sys
import pygame
import math
import pyganim as pa
import lib.spritesheetgaps as spritesheet

# game starts
pygame.init()
pygame.font.init()


pygame.display.set_caption('Game')
size = width, height = 500, 500
screen = pygame.display.set_mode(size)

colorkey = (94, 129, 162)  # background color of spritesheet
st = spritesheet.spritesheet('pixels/small_spritesheet_by_kenney_nl.png')
sprite_dim_players = [
                        pygame.Rect((0,0), (21,21)),
                        pygame.Rect((0,69), (21,21))
                        ]
sprites_strips = [st.load_strip(sprite_dim_players[i], 5, gap=2, colorkey=colorkey) for i in range(2)]
anim_delay = 0.2
# jic put the sprites in a dictionary
player_sprites = [
        {
        'running_right': [sprites[1], sprites[2], sprites[3]],
        'idle': [sprites[0]],
        'jumping_right': [sprites[4]]
        }
        for sprites in sprites_strips
]
for sprites in player_sprites:
    sprites['running_left'] = [ pygame.transform.flip(sprite, 1, 0) for sprite in sprites['running_right'] ]
    sprites['jumping_left'] = [ pygame.transform.flip(sprite, 1, 0) for sprite in sprites['jumping_right'] ]

print(player_sprites)

anim_delay = 0.5

player_animations = [
        {
            'run_left_obj': pa.PygAnimation([(sprite, anim_delay) for sprite in sprites['running_left']]),
        'run_right_obj': pa.PygAnimation([(sprite, anim_delay) for sprite in sprites['running_right']])  # generates a list of tuples and create an animation object
        }
        for sprites in player_sprites
]
#player_animations[1]['run_left_obj'].blit(screen, ((100,100),(21,21)))

clock = pygame.time.Clock()
tt = 0
image = pygame.Surface((21, 21))
image.fill(colorkey)
image.set_colorkey(colorkey)
background = screen.copy()
player_animations[0]['run_left_obj'].play()

while True:
    dt = clock.tick(30)
    tt += dt

    # keyboard events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

#moving_sprites = pygame.sprite.Group()
#
#    # drawing all sprites
#    moving_sprites.update()
#    moving_sprites.draw()

    player_animations[0]['run_left_obj'].blit(screen, ((100,100),(21,21)))
    screen = background
    pygame.display.flip()

    print('Time passed: {}'.format(tt))
