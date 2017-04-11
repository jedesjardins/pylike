from engine.ecs import Component

class Label(Component):
    def __init__(self, label, name=''):
        self.label = label
        self.name = name