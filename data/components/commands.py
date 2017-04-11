from engine.ecs import Component
from engine.command import Command
import data

class Commands(Component):

    def __init__(self, actions):
        self.key_commands = {}
        self.key_options = {}
        self.past_commands = []

        for key, options in actions.items():
            # if a key has a specific action
            if 'filter' in options:
                self.key_options[key] = options['filter']
            # map key to commands
            self.key_commands[key] = []
            for command_loc in options['list']:
                if '.' in command_loc:
                    system, command_name, *_ = command_loc.split('.')
                    command = getattr(getattr(data.systems, system), command_name)
                else:
                    command = getattr(self, command_loc)

                self.key_commands[key].append(command)