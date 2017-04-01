from engine.ecs import Component

class Counter(Component):

    def __init__(self, value=0):
        self.value = value
