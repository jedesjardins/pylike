
from engine.ecs import Component

class Position(Component):

    def __init__(self, x=0, y=0):
        self.x=x
        self.y=y 