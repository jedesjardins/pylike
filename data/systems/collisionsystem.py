# TODO(jhives): change from keys to actions or something?

from engine.ecs import System
from data.components import Position, Hitbox, Undo
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from engine import Quadtree
from pygame import Rect

def undo_collision(undo):
    for command in undo.act_list:
        command.undo()


def get_hitbox_rect(position, hitbox):
    new_rect = hitbox.rect.copy()
    new_rect.center = position.x, position.y - hitbox.y_offset/2
    return new_rect

a = 0

class CollisionSystem(System):

    def update(self, game):
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
                undo = self.entity_manager.component_for_entity(e, Undo)
            except NonexistentComponentTypeForEntity:
                undo = None

            for c in qt.retrieve(hb):
                chitbox = self.entity_manager.component_for_entity(c, Hitbox)
                cposition = self.entity_manager.component_for_entity(c, Position)
                chb = get_hitbox_rect(cposition, chitbox)

                if e != c and hb.colliderect(chb) and undo:
                    undo_collision(undo)


            
                    
    def draw(self, viewport):
        pass