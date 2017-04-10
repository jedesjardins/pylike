from engine.state import State
from engine.make import Maker
from engine.viewport import Viewport
from engine.world import World
import engine.font as Font
import engine.ecs as ecs
from data.systems import *
import pygame

class MenuState(State):

    def __init__(self):
        super().__init__()
        self.entity_manager = ecs.EntityManager()
        self.system_manager = ecs.SystemManager(self.entity_manager)

        # systems
        self.system_manager.add_system(CommandSystem(), 0)
        self.system_manager.add_system(MenuSystem(), 0)
        """
        self.system_manager.add_system(MovementSystem(), 1)
        self.system_manager.add_system(StateSystem(), 1)
        self.system_manager.add_system(AnimationSystem(), 1)
        self.system_manager.add_system(CollisionSystem(), 2)
        self.system_manager.add_system(DrawSystem(), 3)
        """
        
        # create starting items
        self.maker = Maker(self.entity_manager, 'data/entities')
        self.maker["MainMenu"](pos=None)

        self.text_image = Font.get_text_image('The Menu Bitch', 'Minecraft.ttf', 50)
        # create viewport
        self.viewport = Viewport()

    def update(self, dt, keys):
        game = {'dt': dt, 'keys': keys, 'viewport': self.viewport, 
            'play_flag': True, 'next_state': None, 'push_state': None}

        self.system_manager.update(game)

        play_flag = game['play_flag']
        next_state = game['next_state']
        push_state = game['push_state']

        self.viewport.update()
        #self.world.update(self.viewport)

        return play_flag, next_state, push_state

    def draw(self):
        # self.viewport.screen.blit(self.text_image, (0, 0))
        self.system_manager.draw(self.viewport)
        

    def clear(self):
        self.viewport.push((255,255,255))