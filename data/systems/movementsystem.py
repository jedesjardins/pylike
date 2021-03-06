from engine.ecs import System
from engine import Command
from data.components import Position
from engine.ecs.exceptions import NonexistentComponentTypeForEntity

class MovementSystem(System):

    class MoveUp(Command):
        def __init__(self, e, em, game):
            self.position = em.component_for_entity(e, Position)
            self.oy = self.position.y
            self.dt = game['dt']

        def do(self):
            self.position.y += 2

        def undo(self):
            self.position.y = self.oy

    class MoveDown(Command):
        def __init__(self, e, em, game):
            self.position = em.component_for_entity(e, Position)
            self.oy = self.position.y
            self.dt = game['dt']

        def do(self):
            self.position.y -= 2

        def undo(self):
            self.position.y = self.oy

    class MoveLeft(Command):
        def __init__(self, e, em, game):
            self.position = em.component_for_entity(e, Position)
            self.ox = self.position.x
            self.dt = game['dt']

        def do(self):
            self.position.x -= 2

        def undo(self):
            self.position.x = self.ox

    class MoveRight(Command):
        def __init__(self, e, em, game):
            self.position = em.component_for_entity(e, Position)
            self.ox = self.position.x
            self.dt = game['dt']

        def do(self):
            self.position.x += 2

        def undo(self):
            self.position.x = self.ox