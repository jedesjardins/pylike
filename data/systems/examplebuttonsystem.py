from engine.ecs import System
from data.components import Clickable
from engine.ecs.exceptions import NonexistentComponentTypeForEntity

class ButtonSystem(System):

    def update(self, dt, keys):
        if 'd' in keys and keys['d'] == 'down':
            for e, clickable in self.entity_manager.pairs_for_type(Clickable):
                clickable.action.do()
        if 's' in keys and keys['s'] == 'down':
            for e, clickable in self.entity_manager.pairs_for_type(Clickable):
                clickable.action.undo()

    def draw(self):
        pass