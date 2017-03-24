
import pygame

class Viewport(object):
    """ Translates coordinates from the gamespace to the surface coordinate
        space"""

    def __init__(self, point=(0, 0), size=(200, 150), resolution=(800,600)):

        self.screen = pygame.display.set_mode(resolution)
        self.screen_size = resolution
        self.x, self.y = point
        self.w, self.h = size
        self.scale = resolution[0] / size[0]


    def setPosition(self, point=(0, 0)):
        self.x, self.y = point

    def setSize(self, size=(800, 600)):
        self.screen = pygame.display.set_mode(size)
        self.w, self.h = size

    def update(self):
        pass

    # TODO(jhives): rename this? 
    def draw(self):
        # self.screen.fill((0,0,0))
        pygame.display.flip()
        self.screen.fill((0,0,0))

    def draw_image(self):
        pass

    def draw_rect(self, rect):
        pygame.draw.rect(self.screen, (255, 255, 255), self.translate_rect(rect))

    def center_on(point=(0,0), size=(0,0)):
        pass

    def zoom_in(self, percentage):
        pass

    def zoom_out(self, percentage):
        pass

    def translate_rect(self, rect):
        x, y, w, h = rect[0], rect[1], rect[2], rect[3]
        scale = self.scale

        aw, ah = scale * w, scale * h

        ax = scale * (x - self.x)
        ay = self.screen_size[1] - (scale * (y - self.y)) - ah

        trans_rect = (ax, ay, scale*w, scale*h)
        
        return trans_rect


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
