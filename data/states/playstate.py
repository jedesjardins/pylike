from engine.state import State
from engine.make import Maker
from engine.viewport import Viewport
from engine.world import World
import engine.ecs as ecs
from data.systems import *
from data.components import Position, Commands
import pygame

class PlayState(State):

    def __init__(self):
        super().__init__()
        self.entity_manager = ecs.EntityManager()
        self.system_manager = ecs.SystemManager(self.entity_manager)

        # systems
        self.system_manager.add_system(CommandSystem(), 0)
        self.system_manager.add_system(MovementSystem(), 1)
        self.system_manager.add_system(StateSystem(), 1)
        self.system_manager.add_system(AnimationSystem(), 1)
        self.system_manager.add_system(CollisionSystem(), 2)
        self.system_manager.add_system(DeleteSystem(), 2)
        self.system_manager.add_system(DrawSystem(), 3)
        
        # create starting items
        self.maker = Maker(self.entity_manager, 'data/entities')
        self.player = self.maker["Player"]("Detective.png", pos=(12, 12))
        e2 = self.maker["Player"]("Detective.png", pos=(36, 12))
        self.entity_manager.remove_component(e2, Commands)
        self.maker["Box"](pos=(12, 36))

        # create viewport and world
        self.viewport = Viewport()
        self.viewport.lock_on(self.entity_manager.component_for_entity(self.player, Position))
        self.world = World()

    def update(self, game):
        keys = game['keys']
        if 'p' in keys and keys['p'] == 'down':
            game['state_change'] = [('push', 'PauseState')]
        if 'q' in keys:
            game['_running'] = False

        game['viewport'] = self.viewport
        game['world'] = self.world

        self.system_manager.update(game)

        self.viewport.update()
        self.world.update(self.viewport)

    def draw(self):
        self.viewport.draw_image(self.world.image, pos=self.world.position)
        self.system_manager.draw(self.viewport)

    def clear(self):
        self.viewport.push()