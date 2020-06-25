## A 2D platformer game written using pygame
![Level A](https://raw.githubusercontent.com/Dinarin/2d-platformer-pygame/develop/images/level_a.gif "Level A")

![Level B](https://raw.githubusercontent.com/Dinarin/2d-platformer-pygame/develop/images/level_b.gif "Level B")
### Features:
- Two moving player characters in a 1008x1008px window:
    - blue one is controlled with arrow keys;
    - yellow one is controlled with wasd keys;
    - they can jump on tiles;
    - they treat each other as rectangular obstacles;
    - they can pick up bonuses;
- Reading symmetrical map layouts from text file;
- Reading tile images from a single spritesheet;
- Reading tileset names from a tileset python file;
- Reading level number from command line and loading corresponding level from levels folder.

#### To do:
- Sound effects;
- Scoreboard;
- Using circles for player collisions.

### Prerequisites:
- Python >= 2.7 or PyPy >= 6.0.0;
- pygame >=1.9.6.

### How to run:
- Clone or download the repository;
- Run the file main_game.py using Python 3.

### Credits:
- spritesheet module - https://www.pygame.org/wiki/Spritesheet
- pyganim module - http://inventwithpython.com/pyganim
- game assets - http://www.kenney.nl
