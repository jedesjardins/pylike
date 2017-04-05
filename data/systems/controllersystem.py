from engine.ecs import System
from data.components import Controls, Actions
from engine.ecs.exceptions import NonexistentComponentTypeForEntity

class ControllerSystem(System):
    
    def update(self, game):
        dt = game['dt']
        keys = game['keys']

        for e, controls in self.entity_manager.pairs_for_type(Controls):

            try:
                actions = self.entity_manager.component_for_entity(e, Actions)
            except NonexistentComponentTypeForEntity:
                continue

            for action, key_list in controls.actions.items():
                all_held = True
                for key in key_list:
                    if not (key in keys and (keys[key] == 'held' or keys[key] == 'down')):
                        all_held = False
                
                # if key in keys and keys[key] == 'held':
                if all_held:
                    actions.actions.append(action)
                

    def draw(self, viewport):
        pass