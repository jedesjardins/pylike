import pygame
from .chunk import Chunk
from pygame import Rect
import numpy as np


def touching_boundary(rect1, rect2):
    union = rect1.union(rect2)

    if union.w > rect1.w or union.h > rect1.h:
        return True

    return False

class World(object):
    def __init__(self, pos=(0, 0)):
        self.position = pos
        self.size_in_chunks = (6, 4)
        self.tilesheet = pygame.image.load("resources/Tileset.png")
        self.tile_frame = Rect(0, 0, 24, 24)
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
                self.grid[yi+y][xi+x] = chunk[7-yi][xi]



    def update_grid(self):
        for x in range(0, self.size_in_chunks[0] * Chunk.size):
            for y in range(0, self.size_in_chunks[1] * Chunk.size):
                self.grid[y][x] = 0

    def update_image(self):
        map_rect = self.image.get_rect()

        dest_rect = self.tile_frame.copy()
        src_rect = self.tile_frame.copy()
        for y in range(0, self.size_in_chunks[1] * Chunk.size):
            for x in range(0, self.size_in_chunks[0] * Chunk.size):
                dest_rect.x = x * 24
                dest_rect.y = map_rect.h - y * 24 - 24
                src_rect.x = self.grid[y][x] * 24
                self.image.blit(self.tilesheet, dest_rect, src_rect)


    def update(self, viewport):
        map_rect = self.image.get_rect().copy()
        map_rect.center = self.position

        if touching_boundary(map_rect, viewport.rect):
            self.update_chunks()
            self.update_image()
            x, y = viewport.get_position()
            self.position = (x-x%Chunk.size, y-y%Chunk.size)

    def update_chunks(self):
        wx = self.position[0]
        wy = self.position[1]
        mx = int(self.size_in_chunks[0]/2)
        my = int(self.size_in_chunks[1]/2)

        for y in range(0, self.size_in_chunks[1]):
            for x in range(0, self.size_in_chunks[0]):
                chunk = Chunk((wx+x-mx)*Chunk.size, (wy+y-my)*Chunk.size)
                self.place_chunk(chunk, x*Chunk.size, y*Chunk.size)







