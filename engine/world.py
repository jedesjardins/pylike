import pygame
from .chunk import Chunk
from pygame import Rect
import numpy as np
import math
import random
from copy import deepcopy


def touching_boundary(rect1, rect2):
    union = rect1.union(rect2)

    if union.w > rect1.w or union.h > rect1.h:
        return True

    return False

def create_world(type='infinite', pos=(0, 0), seed=0):
    if type == 'infinite':
        return World(pos)
    elif type == 'dungeon':
        return DWorld(pos, seed)

class DWorld(object):

    def __init__(self, pos=(0,0), seed=0):
        self.position = pos
        self.seed = seed
        self.tilesheet = pygame.image.load("resources/Tileset.png")
        self.size = (60, 44)
        self.tile_size = (24, 24)
        self.grid = np.empty([self.size[1], self.size[0]])
        self.grid.fill(1)

        for y in range(0, self.size[1]):
            self.grid[y][0] = 0
            self.grid[y][self.size[0]-1] = 0

        for x in range(0, self.size[0]):
            self.grid[0][x] = 0
            self.grid[self.size[1]-1][x] = 0

        self.populate()

        self.image = pygame.Surface((
                self.tile_size[0] * self.size[0],
                self.tile_size[1] * self.size[1]))

        self.update_image()

    def populate(self):

        random.seed(self.seed)

        for y in range(1, self.size[1]-1):
            for x in range(1, self.size[0]-1):
                self.grid[y][x] = random.randint(0,1)

        
        for i in range(0, 2):
            old_grid = self.grid
            self.grid = deepcopy(old_grid)

            for y in range(1, self.size[1]-1):
                for x in range(1, self.size[0]-1):
                    alive, dead = self.check_neighbors(old_grid, x, y)

                    if self.grid[y][x] == 1:
                        if dead >= 5:
                            self.grid[y][x] = 0
                        else:
                            self.grid[y][x] = 1
                    else:
                        if dead >= 4:
                            self.grid[y][x] = 0
                        else:
                            self.grid[y][x] = 1

    def check_neighbors(self, grid, x, y):
        alive = 0
        dead = 0

        for ry in range(y-1, y+2):
            for rx in range(x-1, x+2):
                if rx == x and ry == y:
                    continue

                if grid[ry][rx] == 1:
                    alive += 1
                else:
                    dead += 1

        return (alive, dead)

    def point_to_tile(self, point):
        x, y = point

        tile_x_off = int((x - self.position[0])//24 + self.size[0]/2)
        tile_y_off = int((y - self.position[1])//24 + self.size[1]/2)
        #print(self.position, point, (tile_x_off, tile_y_off))
        return (tile_x_off, tile_y_off)

    def tile_to_point(self, tile):
        x, y = tile

        x_pos = self.position[0] + (x - self.size[0]/2)*24 + 12
        y_pos = self.position[1] + (y - self.size[1]/2)*24 + 12

        return (x_pos, y_pos)

    def get_collision(self, rect):
        start_x, start_y = self.point_to_tile(rect.topleft)
        end_x, end_y = self.point_to_tile(rect.bottomright)

        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                try:
                    if self.grid[y][x] == 0:
                        return True
                except IndexError:
                    # the object isn't within the world space anymore
                    return False

        return False

    def update(self, viewport):
        pass

    def update_image(self):
        map_rect = self.image.get_rect()

        dest_rect = Rect(0, 0, *self.tile_size)
        src_rect = Rect(0, 0, *self.tile_size)
        for y in range(0, self.size[1]):
            for x in range(0, self.size[0]):
                dest_rect.x = x * 24
                dest_rect.y = map_rect.h - y * 24 - 24
                src_rect.x = self.grid[y][x] * 24
                self.image.blit(self.tilesheet, dest_rect, src_rect)

    def empty_position(self):
        for y in range(0, self.size[1]):
            for x in range(0, self.size[0]):
                if self.grid[y][x] == 1:
                    return self.tile_to_point((x, y))

class World(object):
    def __init__(self, pos=(0, 0)):
        self.position = pos
        self.size_in_chunks = (6, 4)
        self.tilesheet = pygame.image.load("resources/Tileset.png")
        self.tile_size = (24, 24)
        self.image = pygame.Surface((
                self.tile_size[0] * self.size_in_chunks[0] * Chunk.size,
                self.tile_size[1] * self.size_in_chunks[1] * Chunk.size))

        width = self.size_in_chunks[0] * Chunk.size
        height = self.size_in_chunks[1] * Chunk.size
        self.grid = np.empty([height, width])
        self.grid.fill(1)

        # self.place_chunk(Chunk())
        """
        for y in range(0, self.size_in_chunks[1]):
            for x in range(0, self.size_in_chunks[0]):
                print(x, y)
                self.place_chunk(Chunk(), x*Chunk.size, y*Chunk.size)
        """
        
        self.update_chunks()
        self.update_image()

    # unused
    def update_grid(self):
        for x in range(0, self.size_in_chunks[0] * Chunk.size):
            for y in range(0, self.size_in_chunks[1] * Chunk.size):
                self.grid[y][x] = 0

    def update(self, viewport):
        map_rect = self.image.get_rect().copy()
        map_rect.center = self.position

        if touching_boundary(map_rect, viewport.rect):
            x, y = viewport.get_position()
            self.position = (x-x%24, y-y%24)
            self.update_chunks()
            self.update_image()

    def place_chunk(self, chunk, x=0, y=0):
        for yi in range(0, Chunk.size):
            for xi in range(0, Chunk.size):
                self.grid[yi+y][xi+x] = chunk[7-yi][xi]

    def update_chunks(self):
        wx = self.position[0]
        wy = self.position[1]

        for y in range(0, self.size_in_chunks[1]):
            for x in range(0, self.size_in_chunks[0]):
                chunk = Chunk(wx/24+x*Chunk.size, wy/24+y*Chunk.size)
                self.place_chunk(chunk, x*Chunk.size, y*Chunk.size)

    def update_image(self):
        map_rect = self.image.get_rect()

        dest_rect = Rect(0, 0, *self.tile_size)
        src_rect = Rect(0, 0, *self.tile_size)
        for y in range(0, self.size_in_chunks[1] * Chunk.size):
            for x in range(0, self.size_in_chunks[0] * Chunk.size):
                dest_rect.x = x * 24
                dest_rect.y = map_rect.h - y * 24 - 24
                src_rect.x = self.grid[y][x] * 24
                self.image.blit(self.tilesheet, dest_rect, src_rect)

    def point_to_tile(self, point):
        x, y = point

        tile_x_off = int((x - self.position[0])//24 + (self.size_in_chunks[0] * Chunk.size)/2)
        tile_y_off = int((y - self.position[1])//24 + (self.size_in_chunks[1] * Chunk.size)/2)

        return (tile_x_off, tile_y_off)


    def get_collision(self, rect):

        start_x, start_y = self.point_to_tile(rect.topleft)
        end_x, end_y = self.point_to_tile(rect.bottomright)

        for y in range(start_y, end_y + 1):
            for x in range(start_x, end_x + 1):
                try:
                    if self.grid[y][x] == 0:
                        return True
                except IndexError:
                    # the object isn't within the world space anymore
                    return False


        return False


