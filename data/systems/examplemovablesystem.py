from engine.ecs import System
from engine import Command
from data.components import Actions, Position, Undo
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

        for e, actions in self.entity_manager.pairs_for_type(Actions):
            try:
                position = self.entity_manager.component_for_entity(e, Position)
            except NonexistentComponentTypeForEntity:
                continue

            try:
                undo = self.entity_manager.component_for_entity(e, Undo)
                undo.act_list = []
            except NonexistentComponentTypeForEntity:
                undo = None

            action_list = [action_status[0] for action_status in actions.act_list if action_status[1] != 'end']

            for action in action_list:
                if action == 'walk_up':
                    m = self.MoveUp(position, 2)
                    m.do()
                    if undo: undo.act_list.append(m)

                if action == 'walk_down':
                    m = self.MoveDown(position, 2)
                    m.do()
                    if undo: undo.act_list.append(m)

                if action == 'walk_left':
                    m = self.MoveLeft(position, 2)
                    m.do()
                    if undo: undo.act_list.append(m)

                if action == 'walk_right':
                    m = self.MoveRight(position, 2)
                    m.do()
                    if undo: undo.act_list.append(m)

    def draw(self, viewport):
        pass