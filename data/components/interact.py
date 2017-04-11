from engine.ecs import Component
from engine.command import Command
import data
import pygame

class Interact(Component):

    def __init__(self, type_commands):
        self.is_interacting = False
        self.type_commands = {}

        
        for label, command_list in type_commands.items():
            # map key to commands
            self.type_commands[label] = []
            for command_loc in command_list:
                if '.' in command_loc:
                    system, command_name, *_ = command_loc.split('.')
                    command = getattr(getattr(data.systems, system), command_name)
                else:
                    command = getattr(self, command_loc)

                self.type_commands[label].append(command)