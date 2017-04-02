from engine.ecs import System
from data.components import Sprite, Position
from engine.ecs.exceptions import NonexistentComponentTypeForEntity

class SpriteSystem(System):

    def update(self, dt, keys):
        pass

    def draw(self, viewport):
        for e, sprite in self.entity_manager.pairs_for_type(Sprite):
            viewport.draw_image(sprite.image)