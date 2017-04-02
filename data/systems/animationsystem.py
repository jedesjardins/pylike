from engine.ecs import System
from data.components import Animation, Controlled
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from pygame import Rect

class AnimationSystem(System):

    def change_frame_rect(self, animation, x, y):
        r = animation.curr_frame_rect
        r.x = x * r.w
        r.y = y * r.h

    def handle_key(self, animation, dt, keys, key, direction):
        if keys[key] == 'down':
            # start animation
            animation.elapsed_time = animation.animation['length']/len(animation.animation['frames'])
            animation.animation = animation.animations[direction]
            animation.frame = animation.animation['frames'][1]

            print(animation.elapsed_time, animation.frame)
            
        elif keys[key] == 'held':
            animation.elapsed_time += dt

        elif keys[key] == 'up':
            animation.elapsed_time = 0

    def update(self, dt, keys):
        for e, animation in self.entity_manager.pairs_for_type(Animation):
            try:
                controlled = self.entity_manager.component_for_entity(e, Controlled)
            except NonexistentComponentTypeForEntity:
                # TODO(jhives): adapt to ai somehow
                continue

            for action, key_value in controlled.actions.items():
                if key_value in keys:
                    self.handle_key(animation, dt, keys, key_value, action)

            frame_length = animation.animation['length']/len(animation.animation['frames'])
            frame_index = int((animation.elapsed_time // frame_length) % 4)
            animation.frame = animation.animation['frames'][frame_index]
            self.change_frame_rect(animation, animation.frame%3, animation.frame//3)

                    

    def draw(self, viewport):
        pass