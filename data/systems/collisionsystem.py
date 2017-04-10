
# TODO(jhives): change from keys to actions or something?

from engine.ecs import System
from data.components import Position, Hitbox, Commands, Collision, Label
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from engine.quadtree import Quadtree
from engine.command import Command
from pygame import Rect

def get_hitbox_rect(position, hitbox):
    new_rect = hitbox.rect.copy()
    new_rect.center = position.x, position.y - hitbox.y_offset/2
    return new_rect

class CollisionSystem(System):

    class Collide(Command):
        def __init__(self, e, em, game):
            self.commands = em.component_for_entity(e, Commands)

        def do(self):        
            for command in self.commands.past_commands:
                command.undo()

        def undo(self):
            for command in self.commands.past_commands:
                command.do()

    class CollideItem(Command):
        def __init__(self, e, em, game):
            pass

        def do(self):
            pass

    def entity_collisions(self, game):
        dt = game['dt']
        keys = game['keys']
        qt = Quadtree(Rect(0, 0, 100, 100))
        entities = []

        # fill quadtree
        for e, hitbox in self.entity_manager.pairs_for_type(Hitbox):
            try:
                position = self.entity_manager.component_for_entity(e, Position)
            except NonexistentComponentTypeForEntity:
                continue

            # put all hitboxes centered on position into the quadtree as 
            # TODO: How do I get the screen dimensions? Maybe pass game datastructure?

            entities.append(e)
            qt.insert(e, get_hitbox_rect(position, hitbox))


        # iterate all objects and resolve collisions
        for e in entities:
            hitbox = self.entity_manager.component_for_entity(e, Hitbox)
            position = self.entity_manager.component_for_entity(e, Position)

            hb = get_hitbox_rect(position, hitbox)

            try:
                collision = self.entity_manager.component_for_entity(e, Collision)
            except NonexistentComponentTypeForEntity:
                collision = None

            for c in qt.retrieve(hb):
                chitbox = self.entity_manager.component_for_entity(c, Hitbox)
                cposition = self.entity_manager.component_for_entity(c, Position)
                chb = get_hitbox_rect(cposition, chitbox)

                try:
                    label = self.entity_manager.component_for_entity(c, Label).label
                except NonexistentComponentTypeForEntity:
                    label = ''

                if e != c and hb.colliderect(chb) and collision:
                    if label in collision.type_commands:
                        for command in collision.type_commands[label]:
                            c = command(e, self.entity_manager, game)
                            c.do()

    def world_collision(self, game):
        dt = game['dt']
        keys = game['keys']
        world = game['world']

        for e, hitbox in self.entity_manager.pairs_for_type(Hitbox):
            try:
                position = self.entity_manager.component_for_entity(e, Position)
            except NonexistentComponentTypeForEntity:
                continue

            try:
                collision = self.entity_manager.component_for_entity(e, Collision)
            except NonexistentComponentTypeForEntity:
                collision = None

            hb = hitbox.rect.copy()
            hb.center = position.x, position.y - hitbox.y_offset/2

            if world.get_collision(hb) and collision:
                if 'world' in collision.type_commands:
                    for command in collision.type_commands['world']:
                        c = command(e, self.entity_manager, game)
                        c.do()

    def update(self, game):
        self.entity_collisions(game)

        if 'world' in game:
            self.world_collision(game)