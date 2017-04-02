from engine.ecs import System
from data.components import Sprite, Position, Animation
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from pygame import Rect

class DrawSystem(System):

    def update(self, dt, keys):
        pass

    def draw(self, viewport):
        for e, sprite in self.entity_manager.pairs_for_type(Sprite):
            try:
                position = self.entity_manager.component_for_entity(e, Position)
                x, y = position.x, position.y
            except NonexistentComponentTypeForEntity:
                x, y = (0, 0)

            try:
                animation = self.entity_manager.component_for_entity(e, Animation)
                frame_rect = animation.curr_frame_rect
            except NonexistentComponentTypeForEntity:
                frame_rect = sprite.image.get_rect()


            viewport.draw_image(sprite.image, frame_rect, (x, y))