
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

    def fill(self):
        for y in range(0, Chunk.size):
            for x in range(0, Chunk.size):
                rand = noise((x+self.x)/8, (y+self.y)/8, .1, octaves=2)
                if rand < .40 and rand > -.40:
                    value = 1
                else:
                    value = 0 
                self.grid[Chunk.size-1-y][x] = value

    def __getitem__(self, y):
        return self.grid[y]