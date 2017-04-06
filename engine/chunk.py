
from .perlinnoise import PerlinNoise

class Chunk(object):
    size = 8
    def __init__(self, x=None, y=None):
        if x == None or y == None:
            self.grid = \
            [[0,0,0,1,1,0,0,0], 
             [0,1,1,1,1,1,1,0],
             [0,1,1,1,1,1,1,0], 
             [1,1,1,1,1,1,1,1], 
             [1,1,1,1,1,1,1,1], 
             [0,1,1,1,1,1,1,0], 
             [0,1,1,1,1,1,1,0], 
             [0,0,0,1,1,0,0,0]]
        else:
            self.grid = \
            [[0,0,0,1,1,0,0,0], 
             [0,0,0,1,1,0,0,0],
             [0,0,0,1,1,0,0,0], 
             [1,1,1,1,1,1,1,1], 
             [1,1,1,1,1,1,1,1], 
             [0,0,0,1,1,0,0,0], 
             [0,0,0,1,1,0,0,0], 
             [0,0,0,1,1,0,0,0]]


    def __getitem__(self, y):
        return self.grid[y]