import pygame
from .chunk import Chunk
from pygame import Rect

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
        self.size_in_chunks = (3, 3)
        self.tilesheet = pygame.image.load("resources/Tileset.png")
        self.tile_frame = Rect(24, 0, 24, 24)
        self.tile_size = (24, 24)
        self.image = pygame.Surface((
                self.tile_size[0] * self.size_in_chunks[0] * Chunk.size,
                self.tile_size[1] * self.size_in_chunks[1] * Chunk.size))

        self.grid = []
        for y in range(0, self.size_in_chunks[1] * Chunk.size):
            self.grid.append([])
            for x in range(0, self.size_in_chunks[0] * Chunk.size):
                self.grid[y].append((x+y)%2)
        
        #self.update_grid()
        self.update_image()

    def update_grid(self):
        for x in range(0, self.size_in_chunks[0] * Chunk.size):
            for y in range(0, self.size_in_chunks[1] * Chunk.size):
                self.grid[y][x] = 0

    def update_image(self):
        dest_rect = self.tile_frame.copy()
        src_rect = self.tile_frame.copy()
        for y in range(0, self.size_in_chunks[1] * Chunk.size):
            for x in range(0, self.size_in_chunks[0] * Chunk.size):
                dest_rect.x, dest_rect.y = x * 24, y * 24
                src_rect.x = self.grid[y][x] * 24
                self.image.blit(self.tilesheet, dest_rect, src_rect)