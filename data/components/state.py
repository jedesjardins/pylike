from engine.ecs import Component

class State(Component):

    def __init__(self, direction, action):
        self.direction = direction
        self.action = action
        self.next_direction = []
        self.next_action = []
        self.lock_direction = False
        self.continue_action = False