from engine.ecs import Component

class Movable(Component):

    def __init__(self, up, down, left, right):
        self.up = up
        self.down = down
        self.left = left
        self.right = right