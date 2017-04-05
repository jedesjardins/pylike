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
                
            actions.actions = []

            for action, key_value in controls.actions.items():
                if key_value in keys and (keys[key_value] == 'held' or keys[key_value] == 'down'):
                    press = keys[key_value]
                    if press == 'held':
                        actions.actions.append((action, 'continue'))
                    elif press == 'down':
                        actions.actions.append((action, 'start'))
                    elif press == 'up':
                        actions.actions.append((action, 'end'))

            print(e, actions.actions)
                

    def draw(self, viewport):
        pass