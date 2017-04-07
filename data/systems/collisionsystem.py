# TODO(jhives): change from keys to actions or something?

from engine.ecs import System
from data.components import Position, Hitbox, Undo
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from engine import Quadtree
from pygame import Rect

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
            hb = hitbox.rect.copy()
            hb.center = position.x, position.y - hitbox.y_offset/2
            qt.insert(e, hb)


        # iterate all objects and resolve collisions
        for e in entities:
            hitbox = self.entity_manager.component_for_entity(e, Hitbox)
            position = self.entity_manager.component_for_entity(e, Position)

            hb = hitbox.rect.copy()
            hb.center = position.x, position.y - hitbox.y_offset/2

            try:
                undo = self.entity_manager.component_for_entity(e, Undo)
            except NonexistentComponentTypeForEntity:
                undo = None

            for c in qt.retrieve(hb):
                chitbox = self.entity_manager.component_for_entity(c, Hitbox)
                cposition = self.entity_manager.component_for_entity(c, Position)
                chb = chitbox.rect.copy()
                chb.center = cposition.x, cposition.y - chitbox.y_offset/2



                if e != c and hb.colliderect(chb) and undo:
                    for command in undo.act_list:
                            command.undo()
                    """
                    print('Collision: {0}, {1}'. format(str(e), str(c)))
                    print('\t', hb, chb)
                    # e.resolve_collision()
                    # c.resolve_collision()
                    """

            
                    
    def draw(self, viewport):
        pass