from engine.ecs import System
from engine import Command
from data.components import Movable, Position
from engine.ecs.exceptions import NonexistentComponentTypeForEntity

class MovableSystem(System):

    class MoveUp(Command):
        def __init__(self, position):
            self.position = position
            self.oy = position.y

        def do(self):
            self.position.y += 5

        def undo(self):
            self.position.y = self.oy

    class MoveDown(Command):
        def __init__(self, position):
            self.position = position
            self.oy = position.y

        def do(self):
            self.position.y -= 5

        def undo(self):
            self.position.y = self.oy

    class MoveLeft(Command):
        def __init__(self, position):
            self.position = position
            self.ox = position.x

        def do(self):
            self.position.x -= 5

        def undo(self):
            self.position.x = self.ox

    class MoveRight(Command):
        def __init__(self, position):
            self.position = position
            self.ox = position.x

        def do(self):
            self.position.x += 5

        def undo(self):
            self.position.x = self.ox

    def update(self, dt, keys):
        for e, movable in self.entity_manager.pairs_for_type(Movable):
            try:
                position = self.entity_manager.component_for_entity(e, Position)
            except NonexistentComponentTypeForEntity:
                continue

            if movable.up in keys and keys[movable.up] == 'held':
                self.MoveUp(position).do()
            if movable.down in keys and keys[movable.down] == 'held':
                self.MoveDown(position).do()
            if movable.left in keys and keys[movable.left] == 'held':
                self.MoveLeft(position).do()
            if movable.right in keys and keys[movable.right] == 'held':
                self.MoveRight(position).do()

            print(position.x, position.y)

    def draw(self):
        pass