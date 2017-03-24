from engine.state import State
from engine import Viewport
import pygame

class MenuState(State):

    def __init__(self):
        # print("\tMenuState, init")
        super().__init__()
        self.viewport = Viewport.Viewport()
        self.x, self.y = (0, 0)

    def handle_events(self, keys):
        if "mousemove" in keys:
            self.x, self.y = keys["mousemove"]

    def update(self, dt):
        pass

    def draw(self):
        # self.viewport.draw_rect((10, 10, 20, 20))
        pygame.draw.line(self.viewport.screen, (255, 255, 255), 
            (self.x, self.y), (400, 300))
        self.viewport.draw()