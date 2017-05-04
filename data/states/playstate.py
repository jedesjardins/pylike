from engine.state import State
from engine.make import Maker
from engine.viewport import Viewport
from engine.world import create_world
import engine.ecs as ecs
from data.systems import *
from data.components import Position, Commands
import random
import pygame

class PlayState(State):

    def __init__(self):
        super().__init__()
        self.entity_manager = ecs.EntityManager()
        self.system_manager = ecs.SystemManager(self.entity_manager)

        # systems
        self.system_manager.add_system(CommandSystem(), 0)
        self.system_manager.add_system(AISystem(), 0)
        self.system_manager.add_system(MovementSystem(), 1)
        self.system_manager.add_system(StateSystem(), 1)
        self.system_manager.add_system(AnimationSystem(), 1)
        self.system_manager.add_system(InteractSystem(), 1)
        self.system_manager.add_system(CollisionSystem(), 2)
        self.system_manager.add_system(DeleteSystem(), 2)
        self.system_manager.add_system(DrawSystem(), 3)
        self.system_manager.add_system(DrawGameTextSystem(), 4)
        self.system_manager.add_system(UIScriptSystem(), 4)

        # create viewport and world
        self.viewport = Viewport()
        self.world = create_world(type='dungeon', seed=1)

        # create starting items
        self.maker = Maker(self.entity_manager, 'data/entities')
        open_points = self.world.empty_position()

        #self.player = self.maker["Player"]("Scientist.png", pos=(open_point))
        self.player = self.maker["Player"]("Rescuer.png", pos=(open_points[4]))
        self.maker["Person"]("lost_person.json", pos=(open_points[2]))
        exit = (open_points[4][0], open_points[4][1]-24)
        self.maker["Exit"]("exit_script", pos=(exit))
        
        self.maker["Sign"](\
            "DANGER:$PLEASE STOP#EXTREMELY UNSAFE$ ",\
            pos=(open_points[3]))
        

        #self.maker["Script_Tile"]("door_script", pos=(open_points[1]))
        
        #self.maker["Chest"]("1", "2", pos=(open_points[random.randint(0, len(open_points))]))
        #self.maker["Key"]("1", pos=(open_points[random.randint(0, len(open_points))]))
        #self.maker["Person"]("Detective.png", pos=(36, 12))
        #self.maker["Box"](pos=(12, 36))
        #self.maker["Potion"](pos=(36, 36))
        #self.maker["Sign"](pos=(-12, -12))

        self.viewport.lock_on(self.entity_manager.component_for_entity(self.player, Position))

    def update(self, game):

        keys = game['keys']
        if 'p' in keys and keys['p'] == 'down':
            game['state_change'] = [('push', 'PauseState')]
        if 'q' in keys:
            game['_running'] = False
        if 't' in keys and keys['t'] == 'down':
            self.world.curr_floor = (self.world.curr_floor + 1) % self.world.size[2]

        game['viewport'] = self.viewport
        game['world'] = self.world

        self.system_manager.update(game)

        self.viewport.update()
        self.world.update(self.viewport)

    def draw(self):
        self.viewport.draw_image(self.world.get_image(), pos=self.world.position)
        self.system_manager.draw(self.viewport)

    def clear(self):
        self.viewport.push()