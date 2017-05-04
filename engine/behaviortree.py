
import json, sys
from data.components import Commands, Position, Label 
import data

class BehaviorTree():

    def __init__(self, tree_json):
        try:
            self.tree = json.load(tree_json)
        except ValueError: 
            print('Failed to read in preset', preset)


        self.root = self.prepare_nodes(self.tree)
        self.blackboard = Blackboard()

    def prepare_nodes(self, node_info):
        if not node_info:
            return

        module = sys.modules[__name__]

        node = Node(node_info['name'])
        node.config = node_info

        node_class = getattr(module, node_info['class'])
        node = node_class(node_info['name'])
        node.config = node_info

        for node_child in node.config["children"]:
            node.children.append(self.prepare_nodes(node_child))

        return node

    def traverse(self, node):
        print(node.name)

        for node_child in node.children:
            self.traverse(node_child)

    def update(self, game, e):
        if not self.root:
            return

        return self.root.update(game, e, self.blackboard)

class Blackboard:

    def __init__(self):
        self._data = {}

    def store(self, node_path, data):
        self._data[node_path] = data

    def fetch(self, node_path):
        if self._data[node_path]:
            return self._data[node_path]

class Node():

    def __init__(self, name=None):
        self.name = name
        self.children = []
        self.config = None

    # returns 'r', 's', 'f', for running, success, and failure
    def update(self, game, e, blackboard):
        return 's'

class Composite(Node):
    pass

# run children until hit failure, 
class Sequence(Composite):
    def update(self, game, e, blackboard):
        for child in self.children:
            res = child.update(game, e, blackboard)

            if res == 'f':
                return 'f'
            if res == 'r':
                return 's'

        return 's'

class Decorator(Node):
    pass

# run the
class AlwaysTrueD(Decorator):
    def update(self, game, e, blackboard):

        if not self.children:
            return 'f'

        res = self.children[0].update(game, e, blackboard)


        if res != 'f':
            return 's'
        else:
            return 'f'

# This is where the real functionality goes
class Leaf(Node):
    pass

def man_distance(pos1, pos2):
    x_off = abs(pos1.x - pos2.x)
    y_off = abs(pos1.y - pos2.y)
    return x_off + y_off

def euc_distance(pos1, pos2):
    x_off = abs(pos1.x - pos2.x)
    y_off = abs(pos1.y - pos2.y)
    return (x_off**2 + y_off**2)**.5

class NearPlayer(Leaf):
    def update(self, game, e, blackboard):
        e_position = blackboard.fetch('em').component_for_entity(e, Position)

        for t, label in blackboard.fetch('em').pairs_for_type(Label):
            if label.name == 'player':
                targ_position = blackboard.fetch('em').component_for_entity(t, Position)
                d = euc_distance(e_position, targ_position)
                if d < 24*5 and d > 36:
                    blackboard.store('current_pos', e_position)
                    blackboard.store('target_pos', targ_position)
                    return 's'
                else:
                    return 'f'

class FindPathToPlayer(Leaf):
    def update(self, game, e, blackboard):
        next_tile, direction = game['world'].find_tile(blackboard.fetch('current_pos'), blackboard.fetch('target_pos'))
        
        if not direction:
            return 'f'
        blackboard.store('next_direction', direction)
        return 's'

class MoveToPlayer(Leaf):
    def update(self, game, e, blackboard):
        next_dir = blackboard.fetch('next_direction')

        print(next_dir)
        if not next_dir:    
            return 'f'

        comm_comp = blackboard.fetch('em').component_for_entity(e, Commands)

        move_system = getattr(data.systems, "MovementSystem")
        state_system = getattr(data.systems, "StateSystem")

        if next_dir == 'up':
            command = getattr(move_system, "MoveUp")
            c = command(e, blackboard.fetch('em'), game)
            c.do()
            comm_comp.past_commands.append(c)
            command = getattr(state_system, "Up")
            c = command(e, blackboard.fetch('em'), game)
            c.do()
        elif next_dir == 'down':
            command = getattr(move_system, "MoveDown")
            c = command(e, blackboard.fetch('em'), game)
            c.do()
            comm_comp.past_commands.append(c)
            command = getattr(state_system, "Down")
            c = command(e, blackboard.fetch('em'), game)
            c.do()
        elif next_dir == 'left':
            command = getattr(move_system, "MoveLeft")
            c = command(e, blackboard.fetch('em'), game)
            c.do()
            comm_comp.past_commands.append(c)
            command = getattr(state_system, "Left")
            c = command(e, blackboard.fetch('em'), game)
            c.do()
        elif next_dir == 'right':
            command = getattr(move_system, "MoveRight")
            c = command(e, blackboard.fetch('em'), game)
            c.do()
            comm_comp.past_commands.append(c)
            command = getattr(state_system, "Right")
            c = command(e, blackboard.fetch('em'), game)
            c.do()