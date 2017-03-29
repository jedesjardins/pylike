from engine import Viewport
from engine import State 
from engine import Maker
import engine.ecs as ecs
from data.systems import *
from data.components import Counter
import pygame

class MenuState(State):

    def __init__(self):
        # print("\tMenuState, init")
        super().__init__()

        # used to make all the entities and shit
        self.maker = Maker()

        self.entity_manager = ecs.EntityManager()
        self.system_manager = ecs.SystemManager(self.entity_manager)

        self.system_manager.add_system(CounterSystem())

        e = self.entity_manager.create_entity()
        self.entity_manager.add_component(e, Counter())


        self.viewport = Viewport.Viewport()

    def handle_events(self, keys):
        if 'q' in keys:
            return False
        return True

    def update(self, dt):
        self.system_manager.update(dt)

    def draw(self):
        self.system_manager.draw()
        #system_manager.draw()?

        # self.viewport.draw_rect((10, 10, 20, 20))
        #pygame.draw.line(self.viewport.screen, (255, 255, 255), 
        #    (self.x, self.y), (400, 300))
        # self.viewport.draw()