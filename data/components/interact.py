from engine.ecs import Component
from engine.command import Command
import pygame

class Interact(Component):

    def __init__(self, type_commands):
        self.is_interacting = False
        self.type_commands = {}
        """
        for type, command_list in type_commands.items():
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
        """