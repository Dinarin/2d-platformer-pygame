import pygame
import os
from lib import visual as vi_

class LevelData:
    """
    Stores level data
    """
    # map encoding
    map_symb = {
            'p': 'player',
            'd': 'grass',
            'f': 'floating grass',
            'b': 'bonus'
            }
    def __init__(self, dim, lvl_img):
        self.dim = dim
        self.obj_map = {}
        self.lvl_img = lvl_img

    def load_map(self, lvl_num):
        # Find path
        maps_path = '../levels/level'
        lvl_path = maps_path + str(lvl_num)
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, lvl_path)

        half_len = self.dim[0]/2
        height = self.dim[1]

        # First line of the file stores all the symbols used
        with open(filename) as f:
            lvl = [line.rstrip('\n') for line in f]
            self.lvl_map = lvl[1:]
            self.symb = lvl[0]
        if (len(self.lvl_map) <= height):  # checking if the level is full
            if (len(self.lvl_map[0]) == half_len):
                for i in range(len(self.lvl_map)):
                    self.lvl_map[i] += self.lvl_map[i][::-1]
            else:
                raise ValueError("Level string is not the right length")
        else:
            raise Exception("Number of lines is {}, bigger than {} in file {} ".format(len(self.lvl_map), height, filename))

    def parse_map(self):
        """
        Method that extracts coordinates from file
        """
        obj_map = {}
        for char in self.symb:
            obj_map[self.map_symb[char]] = []
        x = 0
        y = 0
        for line in self.lvl_map:
            for tile in line:
                for code in self.map_symb:  # comparing to dictionary
                    # there will be a dictionary where classes are keys\
                            #and instances are in a list
                    if tile == code:
                        obj_map[self.map_symb[code]].append((x,y))
                x += 1
            x = 0
            y += 1
        self.obj_map = obj_map

    def set_lvl_images(self, lvl_img):
        """
        Reads a dictionary of lvl images
        """
        self.lvl_img = lvl_img

if __name__ == "__main__":
    dim = (24,24)
    Level1 = LevelData(dim)
    Level1.load_map(1)
    Level1.parse_map()
    print(Level1.obj_map)
