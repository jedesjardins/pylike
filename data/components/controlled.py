from engine.ecs import Component

class Controlled(Component):

    def __init__(self, actions):
        self.actions = actions