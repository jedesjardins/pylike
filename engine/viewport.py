
import pygame
from pygame import Rect

class Viewport(object):
    """ Translates coordinates from the gamespace to the surface coordinate
        space"""

    # TODO(jhives): rework to use pygame.Rect instead of my stuff,
    #               it already has a lot of functionality that I reimplemented,
    #               Probably poorly too.

    def __init__(self, point=(0, 0), size=(400, 300), resolution=(800,600)):

        self.screen = pygame.display.set_mode(resolution)

        self.rect = Rect(*point, *size)
        self.screen_rect = Rect(0, 0, *resolution)
        self.scale = resolution[0] / size[0]


    def set_position(self, point=(0, 0)):
        self.rect.center = point

    def set_resolution(self, resolution=(800, 600)):
        self.screen = pygame.display.set_mode(size)
        self.w, self.h = size

    def update(self):
        pass

    def push(self):
        # self.screen.fill((0,0,0))
        pygame.display.flip()
        self.screen.fill((0,0,0))

    def draw_image(self, image, source=None, pos=None):
        tsrc = source.copy()
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

    def zoom_in(self, percentage):
        pass

    def zoom_out(self, percentage):
        pass

    # TODO(jhives): implement for calculating collisions
    def on_screen(self, rect):
        """ determines if a rect is on screen

        Checks the boundaries of the viewports location against the rect to see
        if the rect has any portion on screen

        Args:
            rect: a 4 element tuple representing a rect

        Returns:
            boolean: True if within the screens boundaries at all
        
        Raises:
            None 
        """
        pass
