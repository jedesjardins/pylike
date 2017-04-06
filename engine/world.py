import pygame
from .chunk import Chunk
from pygame import Rect
import numpy as np

class World(object):
    """
    def __init__(self, pos=(0, 0)):
        self.position = pos
        self.image = None
        self.size_in_chunks = (2, 2)
        self.grid = []
    """
    def __init__(self, pos=(0, 0)):
        self.position = pos
        self.size_in_chunks = (3, 2)
        self.tilesheet = pygame.image.load("resources/Tileset.png")
        self.tile_frame = Rect(24, 0, 24, 24)
        self.tile_size = (24, 24)
        self.image = pygame.Surface((
                self.tile_size[0] * self.size_in_chunks[0] * Chunk.size,
                self.tile_size[1] * self.size_in_chunks[1] * Chunk.size))

        width = self.size_in_chunks[0] * Chunk.size
        height = self.size_in_chunks[1] * Chunk.size
        self.grid = np.empty([height, width])
        self.grid.fill(1)

        # self.place_chunk(Chunk())
        for y in range(0, self.size_in_chunks[1]):
            for x in range(0, self.size_in_chunks[0]):
                self.place_chunk(Chunk(), x*Chunk.size, y*Chunk.size)
        
        #self.update_grid()
        self.update_image()


    def place_chunk(self, chunk, x=0, y=0):
        for yi in range(0, Chunk.size):
            for xi in range(0, Chunk.size):
                print(yi)
                self.grid[yi+y][xi+x] = chunk[7-yi][xi]



    def update_grid(self):
        for x in range(0, self.size_in_chunks[0] * Chunk.size):
            for y in range(0, self.size_in_chunks[1] * Chunk.size):
                self.grid[y][x] = 0

    def update_image(self):
        map_rect = self.image.get_rect()
        print(map_rect)



        dest_rect = self.tile_frame.copy()
        src_rect = self.tile_frame.copy()
        for y in range(0, self.size_in_chunks[1] * Chunk.size):
            for x in range(0, self.size_in_chunks[0] * Chunk.size):
                dest_rect.x = x * 24
                dest_rect.y = map_rect.h - y * 24 - 24
                src_rect.x = self.grid[y][x] * 24
                self.image.blit(self.tilesheet, dest_rect, src_rect)