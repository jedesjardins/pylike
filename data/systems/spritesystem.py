from engine.ecs import System
from data.components import Sprite, Position
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from pygame import Rect

class SpriteSystem(System):

    def update(self, dt, keys):
        pass

    def draw(self, viewport):
        for e, sprite in self.entity_manager.pairs_for_type(Sprite):
            try:
                position = self.entity_manager.component_for_entity(e, Position)
                x, y = position.x, position.y
            except NonexistentComponentTypeForEntity:
                x, y = (0, 0)

            viewport.draw_image(sprite.image, sprite.frame_rect, (x, y))