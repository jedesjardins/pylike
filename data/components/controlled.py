from engine.ecs import Component

class Controlled(Component):

    def __init__(self, up, down, left, right):
        self.up = up
        self.down = down
        self.left = left
        self.right = right