from engine.ecs import Component
from engine.command import Command
import data.components
from data.components import *

class Commands(Component):

    class Interact(Command):
        def __init__(self, e, em, game):
            pass

        def do(self):
            print("Need to implement")

    def __init__(self, actions):
        self.key_commands = {}
        self.past_commands = []
        for key, command_list in actions.items():
            self.key_commands[key] = []
            for command_loc in command_list:
                if '.' in command_loc:
                    system, command_name, *_ = command_loc.split('.')
                    command = getattr(getattr(data.systems, system), command_name)
                else:
                    command = getattr(self, command_loc)

                self.key_commands[key].append(command)