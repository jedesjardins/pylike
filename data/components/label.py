from engine.ecs import Component

class Label(Component):
    def __init__(self, label):
        self.label = label