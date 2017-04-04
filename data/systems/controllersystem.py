from engine.ecs import System
from data.components import Controls, Actions
from engine.ecs.exceptions import NonexistentComponentTypeForEntity

class ControllerSystem(System):
    
    def update(self, game):
        dt = game['dt']
        keys = game['keys']

        for e, controls in self.entity_manager.pairs_for_type(Controls):

            try:
                position = self.entity_manager.component_for_entity(e, Position)
            except NonexistentComponentTypeForEntity:
                continue


            for action, key_list in controls.actions.items():
                pass
                all_held = True
                for key in key_list:
                    if not key in keys and keys[key] == 'held':
                        all_held = False
                
                # if key in keys and keys[key] == 'held':
                if all_held:
                    print(action)
                    """
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