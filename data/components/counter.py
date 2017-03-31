
from engine.ecs import Component

class Counter(Component):

    def __init__(self):
        self.value = 0
