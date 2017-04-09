
from engine.ecs import System
from data.components import Commands, Position
from engine.ecs.exceptions import NonexistentComponentTypeForEntity

class CommandSystem(System):
    
    def update(self, game):
        keys = game['keys']
        for e, commands in self.entity_manager.pairs_for_type(Commands):
            commands.past_commands = []
            for key, command_list in commands.key_commands.items():
                if key in keys:
                    for command in command_list:
                        c = command(e, self.entity_manager, game)
                        c.do()
                        commands.past_commands.append(c)