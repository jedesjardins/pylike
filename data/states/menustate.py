from engine import Viewport
from engine import State 
import engine.ecs as ecs
import pygame

class MenuState(State):

    def __init__(self):
        # print("\tMenuState, init")
        super().__init__()

        self.entity_manager = ecs.EntityManager()
        self.system_manager = ecs.SystemManager(self.entity_manager)

        self.viewport = Viewport.Viewport()

    def handle_events(self, keys):
        if 'q' in keys:
            return False
        return True

    def update(self, dt):
        pass

    def draw(self):
        pass
        #system_manager.draw()?

        # self.viewport.draw_rect((10, 10, 20, 20))
        #pygame.draw.line(self.viewport.screen, (255, 255, 255), 
        #    (self.x, self.y), (400, 300))
        self.viewport.draw()