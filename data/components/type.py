from engine.ecs import Component

class Type(Component):
    def __init__(self, label):
        self.label = label