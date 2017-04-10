from engine import State, Maker, Viewport, World
import engine.ecs as ecs
from data.systems import *
from data.components import Position, Commands
import pygame

class PlayState(State):

    def __init__(self):
        # print("\tMenuState, init")
        super().__init__()
        self.entity_manager = ecs.EntityManager()
        self.system_manager = ecs.SystemManager(self.entity_manager)

        # used to make all the entities and shit
        self.maker = Maker(self.entity_manager, 'data/entities')
        """
        self.system_manager.add_system(ControllerSystem(), 0)
        self.system_manager.add_system(MovableSystem(), 1)
        self.system_manager.add_system(CollisionSystem(), 1)
        """
        self.system_manager.add_system(CommandSystem(), 0)
        self.system_manager.add_system(MovementSystem(), 1)
        self.system_manager.add_system(StateSystem(), 1)
        self.system_manager.add_system(AnimationSystem(), 1)
        self.system_manager.add_system(CollisionSystem(), 2)
        self.system_manager.add_system(DrawSystem(), 3)
        

        e = self.maker["Player"]("Detective.png", pos=(12, 12))
        e2 = self.maker["Player"]("Detective.png", pos=(36, 12))
        self.entity_manager.remove_component(e2, Commands)
        self.maker["Box"](pos=(12, 36))

        self.world = World()

        self.viewport = Viewport()
        # self.viewport.center_on((0, 0))
        self.viewport.lock_on(self.entity_manager.component_for_entity(e, Position))

    def update(self, dt, keys):
        if 'esc' in keys:
            return False

        game = {'dt': dt, 'keys': keys, 
            'viewport': self.viewport, 'world': self.world}

        play_flag = self.system_manager.update(game)

        self.viewport.update()
        self.world.update(self.viewport)

        return play_flag

    def draw(self):
        #self.viewport.screen.blit(self.world.image, pygame.Rect(0, 0, 10, 10))

        self.viewport.draw_image(self.world.image, pos=self.world.position)
        self.system_manager.draw(self.viewport)
        
        # self.viewport.draw_rect((10, 10, 20, 20))
        # pygame.draw.rect(self.viewport.screen, (255, 255, 255), (10, 10, 20, 20))
        self.viewport.push()