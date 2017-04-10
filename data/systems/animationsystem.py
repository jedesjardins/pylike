# TODO(jhives): change from keys to actions or something?

from engine.ecs import System
from data.components import Animation, State, Sprite
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from pygame import Rect

class AnimationSystem(System):

    def change_frame_rect(self, sprite, x, y):
        r = sprite.curr_frame_rect
        r.x = x * r.w
        r.y = y * r.h

    def update(self, game):
        dt = game['dt']

        for e, animation in self.entity_manager.pairs_for_type(Animation):
            try:
                sprite = self.entity_manager.component_for_entity(e, Sprite)
                state = self.entity_manager.component_for_entity(e, State)

            except NonexistentComponentTypeForEntity:
                continue

            state_key = '{0}.{1}'.format(state.action, state.direction)

            action = animation.action_animation[state_key]

            if state.continue_action:
                animation.elapsed_time += dt
            else:
                animation.elapsed_time = 0

            duration = action['duration']
            frame_count = len(action['frames'])
            frame_length = duration/frame_count
            frame_index = int((animation.elapsed_time // frame_length) % frame_count)
            frame_column = sprite.columns
            frame = action['frames'][frame_index]
            self.change_frame_rect(sprite, frame%frame_column, frame//frame_column)
