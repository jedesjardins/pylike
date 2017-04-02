
from engine.ecs import System
from data.components import Counter
from data.components import Position
from engine.ecs.exceptions import NonexistentComponentTypeForEntity

class CounterSystem(System):

    def update(self, dt, keys):
        for e, counter in self.entity_manager.pairs_for_type(Counter):
            counter.value += 1

    def draw(self, viewport):
        for e, counter in self.entity_manager.pairs_for_type(Counter):
            print(counter.value)
