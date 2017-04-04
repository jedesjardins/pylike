# TODO(jhives): change from keys to actions or something?

from engine.ecs import System
from data.components import Animation, Controlled
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from pygame import Rect

class AnimationSystem(System):

    def change_frame_rect(self, animation, x, y):
        r = animation.curr_frame_rect
        r.x = x * r.w
        r.y = y * r.h

    def start_animation(self, animation, action):
        animation.action['elapsed_time'] = animation.action['length']/len(animation.action['frames'])
        animation.action = animation.actions[action]
        animation.frame = animation.action['frames'][1]

    # TODO(jhives): Make this work with three keys held (ex: up, down, right)
    def continue_animation(self, animation, action, dt):
        if action == animation.action['name']:
            animation.action['elapsed_time'] += dt

    def end_animation(self, animation, controlled, keys):
        animation.action['elapsed_time'] = 0
        for action, key_value in controlled.actions.items():
            if key_value in keys and (keys[key_value] == 'down' or keys[key_value] == 'held'):
                self.start_animation(animation, action)
                break

    def handle_key(self, animation, controlled, dt, keys, key, action):

        if keys[key] == 'down':
            self.start_animation(animation, action)
            
        elif keys[key] == 'held':
            self.continue_animation(animation, action, dt)

        elif keys[key] == 'up':
            self.end_animation(animation, controlled, keys)

    def update(self, dt, keys):
        for e, animation in self.entity_manager.pairs_for_type(Animation):
            try:
                controlled = self.entity_manager.component_for_entity(e, Controlled)
            except NonexistentComponentTypeForEntity:
                # TODO(jhives): adapt to ai somehow
                continue

            for action, key_value in controlled.actions.items():
                if key_value in keys:
                    self.handle_key(animation, controlled, dt, keys, key_value, action)

            frame_length = animation.action['length']/len(animation.action['frames'])
            frame_index = int((animation.action['elapsed_time'] // frame_length) % 4)
            animation.frame = animation.action['frames'][frame_index]
            self.change_frame_rect(animation, animation.frame%3, animation.frame//3)
                    
    def draw(self, viewport):
        pass