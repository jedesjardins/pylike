
# TODO(jhives): change from keys to actions or something?

from engine.ecs import System
from data.components import Position, Interact, Inventory, Label, Hitbox
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from engine.quadtree import Quadtree
from engine.command import Command
from pygame import Rect
import math

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
        def __init__(self, e, em, game, e2):
            self.inventory = em.component_for_entity(e, Inventory)
            self.e2 = e2

        def do(self):
            self.inventory.items.append(self.e2)

    def update(self, game):
        all_entities = []
        entities = []
        for e, interact in self.entity_manager.pairs_for_type(Interact):
            all_entities.append(e)
            if not interact.is_interacting:
                continue
            entities.append(e)
            interact.is_interacting = False

        for e in entities:
            try:
                position = self.entity_manager.component_for_entity(e, Position)
                label = self.entity_manager.component_for_entity(e, Label)
                interact = self.entity_manager.component_for_entity(e, Interact)

            except:
                continue

            x, y = position.x, position.y

            for c in all_entities:
                try:
                    cposition = self.entity_manager.component_for_entity(c, Position)
                    clabel = self.entity_manager.component_for_entity(c, Label)
                    cinteract = self.entity_manager.component_for_entity(c, Interact)
                except:
                    continue

                cx, cy = cposition.x, cposition.y

                if e != c and abs(cx-x) < 30 and abs(cy-y) < 30:
                    if label in interact.type_commands:
                        for command in interact.type_commands[clabel]:
                            d = command(e, self.entity_manager, game, c)
                            d.do()

                    if clabel in cinteract.type_commands:
                        for command in cinteract.type_commands[label]:
                            d = command(c, self.entity_manager, game, e)
                            d.do()


            # get all things close to it

            # for each thing, check its type, match it to a command