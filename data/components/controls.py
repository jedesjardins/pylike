from engine.ecs import Component

class Controls(Component):

    def __init__(self, actions):
        self.actions = actions