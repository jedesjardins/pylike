# TODO(jhives): change from keys to actions or something?

from engine.ecs import System
from data.components import Position, Hitbox
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from engine import Quadtree

class CollisionSystem(System):

    def update(self, dt, keys):
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
            hb = hitbox.copy()
            hb.center = position.x, position.y
            qt.insert(e, hb)


        # iterate all objects and resolve collisions
        for e in entities:
            hitbox = self.entity_manager.component_for_entity(e, Hitbox)
            position = self.entity_manager.component_for_entity(e, Position)

            hb = hitbox.copy()
            hb.center = position.x, position.y

            for c in qt.retrieve[hb]:
                chb = self.entity_manager.component_for_entity(c, Hitbox)

                if hb.colliderect(chb):
                    e.resolve_collision()
                    c.resolve_collision()

            
                    
    def draw(self, viewport):
        pass