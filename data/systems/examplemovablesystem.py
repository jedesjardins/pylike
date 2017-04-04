from engine.ecs import System
from engine import Command
from data.components import Controls, Position
from engine.ecs.exceptions import NonexistentComponentTypeForEntity

class MovableSystem(System):

    class MoveUp(Command):
        def __init__(self, position, dp):
            self.position = position
            self.oy = position.y
            self.dp = dp

        def do(self):
            self.position.y += self.dp

        def undo(self):
            self.position.y = self.oy

    class MoveDown(Command):
        def __init__(self, position, dp):
            self.position = position
            self.oy = position.y
            self.dp = dp

        def do(self):
            self.position.y -= self.dp

        def undo(self):
            self.position.y = self.oy

    class MoveLeft(Command):
        def __init__(self, position, dp):
            self.position = position
            self.ox = position.x
            self.dp = dp

        def do(self):
            self.position.x -= self.dp

        def undo(self):
            self.position.x = self.ox

    class MoveRight(Command):
        def __init__(self, position, dp):
            self.position = position
            self.ox = position.x
            self.dp = dp

        def do(self):
            self.position.x += self.dp

        def undo(self):
            self.position.x = self.ox

    def update(self, game):
        dt = game['dt']
        keys = game['keys']

        for e, movable in self.entity_manager.pairs_for_type(Controls):
            try:
                position = self.entity_manager.component_for_entity(e, Position)
            except NonexistentComponentTypeForEntity:
                continue


            for action, keylist in movable.actions.items():
                pass
                # TODO(jhives): change to if every key in list is held, move it
                """
                if keylist in keys and keys[keylist] == 'held':
                    if action == 'walk_up':
                        self.MoveUp(position, 2).do()

                    if action == 'walk_down':
                        self.MoveDown(position, 2).do()

                    if action == 'walk_left':
                        self.MoveLeft(position, 2).do()

                    if action == 'walk_right':
                        self.MoveRight(position, 2).do()
                """

    def draw(self, viewport):
        pass