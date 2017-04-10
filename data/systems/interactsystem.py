
# TODO(jhives): change from keys to actions or something?

from engine.ecs import System
from data.components import Position, Interact
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from engine.quadtree import Quadtree
from engine.command import Command
from pygame import Rect

def get_hitbox_rect(position, hitbox):
    new_rect = hitbox.rect.copy()
    new_rect.center = position.x, position.y - hitbox.y_offset/2
    return new_rect

class InteractSystem(System):

    class Interact(Command):
        def __init__(self, e, em, game):
            self.interact = em.component_for_entity(e, Interact)

        def do(self):
            self.interact.is_interacting = True

    class Pickup(Command):
        def __init__(self, e, em, game):
            self.e = e
            self.em = em

        def do(self):
            print('Implement Pickup')

    def update(self, game):
        for e, interact in self.entity_manager.pairs_for_type(Interact):
            if not interact.is_interacting:
                continue

            # get all things close to it

            # for each thing, check its type, match it to a command