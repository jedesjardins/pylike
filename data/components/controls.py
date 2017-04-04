from engine.ecs import Component

class Controls(Component):

    def __init__(self, actions):
        self.actions = {}
        for action, key_string in actions.items():
            self.actions['action'] = key_string.split('.')