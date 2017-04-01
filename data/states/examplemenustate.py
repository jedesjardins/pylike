from engine import Viewport, State, Maker
from engine import Command
import engine.ecs as ecs
from data.systems import *
# from data.components import Person
import pygame

class MenuState(State):

    def __init__(self):
        # print("\tMenuState, init")
        super().__init__()
        self.entity_manager = ecs.EntityManager()
        self.system_manager = ecs.SystemManager(self.entity_manager)

        # used to make all the entities and shit
        self.maker = Maker(self.entity_manager, 'data/entities')

        #self.system_manager.add_system(CounterSystem())
        #self.system_manager.add_system(ButtonSystem())
        self.system_manager.add_system(MovableSystem())

        # e = self.entity_manager.create_entity()
        # self.entity_manager.add_component(e, Counter())

        # self.maker["Counter"](pos=None);
        self.maker["Person"]('w', 's', 'a', 'd');

        self.viewport = Viewport.Viewport()

    """
    def handle_events(self, keys):
        if 'q' in keys:
            return False
        return self.system_manager.handle_events(keys)
    """

    def update(self, dt, keys):
        if 'q' in keys:
            return False
        return self.system_manager.update(dt, keys)


    def draw(self):
        self.system_manager.draw()
        #system_manager.draw()?

        # self.viewport.draw_rect((10, 10, 20, 20))
        #pygame.draw.line(self.viewport.screen, (255, 255, 255), 
        #    (self.x, self.y), (400, 300))
        # self.viewport.draw()