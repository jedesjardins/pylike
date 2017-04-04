from engine.ecs import System
from data.components import Sprite, Position, Animation
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from pygame import Rect

class DrawSystem(System):

    def update(self, game):
        pass

    def draw(self, viewport):
        # dict maps e -> (image, frame_rect, x, y, z)
        entities = []

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
                frame_rect = sprite.frame_rect

            # subtract because of euclidean space
            # TODO(jhives): this might need to work off the hitbox, as it 
            #               represents the visible part of the sprite.. idk yet
            z = y - frame_rect.h/2

            dest = frame_rect.copy()
            dest.center = x, y

            if dest.colliderect(viewport.rect):
                entities.append((sprite.image, frame_rect, x, y, z))

        for group in sorted(entities, key=lambda entity: entity[4], reverse=True):
            image, rect, x, y, z = group
            viewport.draw_image(image, rect, (x, y))
