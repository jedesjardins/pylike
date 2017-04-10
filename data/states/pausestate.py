from engine.state import State
from engine.viewport import Viewport
import engine.ecs as ecs

class PauseState(State):
    def __init__(self):
        super().__init__()
        self.entity_manager = ecs.EntityManager()
        self.system_manager = ecs.SystemManager(self.entity_manager)

        self.viewport = Viewport()


    def update(self, dt, keys):
        game = {'dt': dt, 'keys': keys, 'viewport': self.viewport, 
            'play_flag': True, 'next_state': None}

        self.system_manager.update(game)

        return True, None, None

    def draw(self):
        pass
        
    def clear(self):
        pass