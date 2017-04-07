
from noise import snoise3 as noise
import numpy as np

class Chunk(object):
    size = 8
    def __init__(self, x=None, y=None):
        #print(x, y)
        if not x:
            x=0
        if not y:
            y=0

        self.x = x
        self.y = y

        self.grid = np.empty([Chunk.size, Chunk.size])
        self.fill()
        """
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
        """

    def fill(self):
        for y in range(0, Chunk.size):
            for x in range(0, Chunk.size):
                if noise((x+self.x)/8, (y+self.y)/8, .1, octaves=2) > -.1:
                    value = 1
                else:
                    value = 0 
                self.grid[Chunk.size-1-y][x] = value



    def __getitem__(self, y):
        return self.grid[y]