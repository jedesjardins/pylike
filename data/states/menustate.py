from engine.state import State
from engine.make import Maker
from engine.viewport import Viewport
from engine.world import World
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

        self.font = pygame.font.Font("resources/fonts/Minecraft.ttf", 50)
        self.text_image = self.font.render("The Menu Bitch", True, (255,255,255))
        # create viewport
        self.viewport = Viewport()

    def update(self, dt, keys):
        if 'enter' in keys and keys['enter'] == 'down':
            return True, 'PlayState'
        if 'esc' in keys and keys['esc'] == 'down':
            return False, None

        game = {'dt': dt, 'keys': keys, 
            'viewport': self.viewport}

        play_flag = self.system_manager.update(game)

        self.viewport.update()
        #self.world.update(self.viewport)

        return play_flag, None

    def draw(self):
        self.viewport.screen.blit(self.text_image, (0, 0))
        self.system_manager.draw(self.viewport)
        self.viewport.push()