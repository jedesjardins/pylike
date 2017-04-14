
import pygame
from pygame import Rect

class Viewport(object):
    """ Translates coordinates from the gamespace to the surface coordinate
        space"""

    # TODO(jhives): rework to use pygame.Rect instead of my stuff,
    #               it already has a lot of functionality that I reimplemented,
    #               Probably poorly too.

    def __init__(self, point=(0, 0), size=(400, 300), resolution=(800,600)):

        self.screen = pygame.display.set_mode(resolution, pygame.DOUBLEBUF, 32)

        self.rect = Rect(*point, *size)
        self.screen_rect = Rect(0, 0, *resolution)
        self.scale = resolution[0] / size[0]

        self.lock = None


    def set_position(self, point=(0, 0)):
        self.rect.center = point

    def get_position(self):
        return self.rect.center

    def set_resolution(self, resolution=(800, 600)):
        self.screen = pygame.display.set_mode(size)
        self.w, self.h = size

    def push(self, color=(0,0,0)):
        # self.screen.fill((0,0,0))
        pygame.display.flip()
        self.screen.fill(color)

    def draw_image(self, image, source=None, pos=None):
        if not source:
            source = image.get_rect()
        if not pos:
            pos = self.rect.center

        tsrc = source.copy()
        tsrc.x, tsrc.y = self.scale * source.x, self.scale * source.y
        tsrc.size = self.scale * source.w, self.scale * source.h

        dest = self.translate_rect(source, pos)
        self.screen.blit(pygame.transform.scale(image, (int(self.scale * image.get_rect().w), int(self.scale * image.get_rect().h))),
                dest, tsrc)

    def translate_rect(self, rect, pos):
        dest = Rect(0, 0, self.scale * rect.w, self.scale * rect.h)
        dest.center = self.translate_pos(pos)
        return dest
        
    def translate_pos(self, pos):
        x, y = pos
        x = self.scale * (x - self.rect.x)
        y = self.screen_rect.h - (self.scale * (y - self.rect.y))
        return (x, y)

    def draw_rect(self, rect):
        pygame.draw.rect(self.screen, (255, 255, 255), self.translate_rect(rect))

    def center_on(self, point=(0,0), size=(0,0)):
        self.rect.center = point

    # TODO(): FIX, Zoom is fucked
    def zoom_in(self, percentage):
        print(self.rect)
        c = self.rect.copy().center
        self.rect.w = self.rect.w * 1.05
        self.rect.h = self.rect.h * 1.05
        self.rect.center = c
        print(self.rect)

    def zoom_out(self, percentage):
        c = self.rect.copy().center
        self.rect.w = self.rect.w * .95
        self.rect.h = self.rect.h * .95
        self.rect.center = c

    # TODO(jhives): implement for calculating collisions
    def on_screen(self, rect):
        pass

    def lock_on(self, position):
        self.lock = position

    def update(self):
        if self.lock:
            self.center_on((self.lock.x, self.lock.y))

    def get_point_position(point):
        x, y = point
