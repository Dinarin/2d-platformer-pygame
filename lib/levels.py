# Level 1
import lib.classes
import lib.pyganim


sprites = SpriteManager('../pixels/small_spritesheet_by_kenney_nl.png',\
        colorkey=True)
sprites.get_strip((...), 4, gap=2, 'player1')
