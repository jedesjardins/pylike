# TODO(jhives): change from keys to actions or something?

from engine.ecs import System
from data.components import Delete, Position
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from engine.quadtree import Quadtree
from engine.command import Command
from pygame import Rect

def get_hitbox_rect(position, hitbox):
    new_rect = hitbox.rect.copy()
    new_rect.center = position.x, position.y - hitbox.y_offset/2
    return new_rect

class DeleteSystem(System):

    class Delete(Command):
        def __init__(self, e, em, game, *_):
            self.e = e
            self.em = em

        def do(self):
            self.em.add_component(self.e, Delete())

    def update(self, game):
        entities = []
        for e, delete in self.entity_manager.pairs_for_type(Delete):
            entities.append(e)

        for e in entities:
            self.entity_manager.remove_component(e, Position)
            self.entity_manager.remove_component(e, Delete)