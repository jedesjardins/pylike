from engine.state import State
from engine.viewport import Viewport
import engine.font as Font
import engine.ecs as ecs

class PauseState(State):
    def __init__(self):
        super().__init__()
        self.entity_manager = ecs.EntityManager()
        self.system_manager = ecs.SystemManager(self.entity_manager)

        self.text = Font.get_text_image('Paused', 'Minecraft.ttf', 50)

        self.viewport = Viewport()


    def update(self, game):
        keys = game['keys']
        if 'p' in keys and keys['p'] == 'down':
            game['state_change'] = [('pop', 1)]
        if 'esc' in keys and keys['esc'] == 'down':
            game['state_change'] = [('pop', 1), ('change', 'MenuState')]

        self.system_manager.update(game)

    def draw(self):
        rect = self.text.get_rect()
        screen_rect = self.viewport.screen.get_rect()
        rect.center = screen_rect.center

        self.viewport.screen.blit(self.text, rect)

        
    def clear(self):
        self.viewport.push()