from engine import State, Maker
from engine.viewport import Viewport
import engine.ecs as ecs
from data.systems import *
import pygame

class PlayState(State):

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
        self.system_manager.add_system(DrawSystem())
        self.system_manager.add_system(AnimationSystem())

        # e = self.entity_manager.create_entity()
        # self.entity_manager.add_component(e, Counter())

        # self.maker["Counter"](pos=None);
        # self.maker["Person"]('w', 's', 'a', 'd');
        self.maker["Actor"]("Detective.png", pos=(0, 0))

        self.viewport = Viewport()
        self.viewport.center_on(point=(0, 0))
        # self.viewport.set_position(point=(0, 0))

    def update(self, dt, keys):
        if 'q' in keys:
            return False
        return self.system_manager.update(dt, keys)


    def draw(self):
        self.system_manager.draw(self.viewport)
        
        # self.viewport.draw_rect((10, 10, 20, 20))
        # pygame.draw.rect(self.viewport.screen, (255, 255, 255), (10, 10, 20, 20))
        self.viewport.push()