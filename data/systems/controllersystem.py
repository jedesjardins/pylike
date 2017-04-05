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
                
            actions.act_list = []

            for action, key_value in controls.actions.items():
                if key_value in keys:
                    press = keys[key_value]
                    if press == 'held':
                        actions.act_list.append((action, 'continue'))
                    elif press == 'down':
                        actions.act_list.append((action, 'start'))
                    elif press == 'up':
                        actions.act_list.append((action, 'end'))
                

    def draw(self, viewport):
        pass