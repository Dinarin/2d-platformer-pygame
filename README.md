## A simple 2D platformer game with two players
![Level A](https://raw.githubusercontent.com/Dinarin/2d-platformer-pygame/develop/images/level_a.gif "Level A")
![Level B](https://raw.githubusercontent.com/Dinarin/2d-platformer-pygame/develop/images/level_b.gif "Level B")
### Features:
- Two animated player characters in a 1008x1008px window:
    - player 1 (blue one) is controlled with wasd keys;
    - player 2 (yellow one) is controlled with arrow keys;
    - they can jump on tiles;
    - they treat each other as rectangular obstacles;
    - they can pick up bonuses;
- Reading symmetrical map layouts from text files;
- Reading tile images from a single spritesheet;
- Reading tileset names from a tileset python file;
- Reading level number from command line and loading corresponding level from levels folder;
- The objective of the game is to collect more bonuses than the opponent;
- Game ends when there is no bonuses left.

### Todo:
- Level editor;
- Easier tileset change;
- Easier level editing;
- Full documentation.

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
