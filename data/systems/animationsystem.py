# TODO(jhives): change from keys to actions or something?

from engine.ecs import System
from data.components import Animation, Actions
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from pygame import Rect

class AnimationSystem(System):

    def change_frame_rect(self, animation, x, y):
        r = animation.curr_frame_rect
        r.x = x * r.w
        r.y = y * r.h

    def start_animation_key(self, animation, action):

        animation.action['elapsed_time'] = animation.action['length']/len(animation.action['frames'])
        animation.action = animation.actions[action]
        animation.frame = animation.action['frames'][1]

    # TODO(jhives): Make this work with three keys held (ex: up, down, right)
    def continue_animation_key(self, animation, action, dt):
        if action == animation.action['name']:
            animation.action['elapsed_time'] += dt

    def end_animation_key(self, animation, controls, keys):
        animation.action['elapsed_time'] = 0
        for action, key_list in controls.actions.items():
            if key_value in keys and (keys[key_value] == 'down' or keys[key_value] == 'held'):
                self.start_animation(animation, action)
                break   

    def handle_key(self, animation, controls, dt, keys, key_list, action):
        if keys[key_list] == 'down':
            self.start_animation(animation, action)
            
        elif keys[key_list] == 'held':
            self.continue_animation(animation, action, dt)

        elif keys[key_list] == 'up':
            self.end_animation(animation, controls, keys)

    def start_animation(self, animation, action):
        animation.action['elapsed_time'] = animation.action['length']/len(animation.action['frames'])
        animation.action = animation.actions[action]
        animation.frame = animation.action['frames'][1]

    # TODO(jhives): Make this work with three keys held (ex: up, down, right)
    def continue_animation(self, animation, action, dt):
        if action == animation.action['name']:
            animation.action['elapsed_time'] += dt

    def end_animation(self, animation, actions):
        animation.action['elapsed_time'] = 0

        for action_status in actions:
            action, status = action_status
            if action == 'strafe': 
                if status == 'end': continue
                else: break
            if status == 'end': continue
            self.start_animation(animation, action)
            break


    def handle_action(self, animation, actions, action, status, dt):
        # true if sliding
        strafe = 'strafe' in [action_status[0] for action_status in actions]

        #
        # Maybe if strafe is detected here just continue the animation
        #

        if status == 'start':
            # start this animation unless the shift button is held

            # if shift key is down
            # continue the current animation
            # else
            self.start_animation(animation, action)

        if status == 'continue':
            # continue this animation if it's name matches the current action
            self.continue_animation(animation, action, dt)
            pass

        if status == 'end':
            # end the animation and switch to another unless the shift button 
            # is held, in witch case, continue on the current animation
            self.end_animation(animation, actions)

    def update(self, game):
        dt = game['dt']
        keys = game['keys']

        for e, animation in self.entity_manager.pairs_for_type(Animation):
            try:
                actions = self.entity_manager.component_for_entity(e, Actions)
            except NonexistentComponentTypeForEntity:
                continue

            # if strafe is held and other buttons are held, continue the action
            if 'strafe' in [action_status[0] for action_status in actions.act_list]:

                if len(actions.act_list) > 1:
                    self.continue_animation(animation, animation.action['name'], dt)
                else:
                    self.end_animation(animation, actions.act_list)
            # 
            else:
                for action_status in actions.act_list:
                    action, status = action_status

                    if action != 'strafe':
                        self.handle_action(animation, actions.act_list, action, status, dt)

            frame_length = animation.action['length']/len(animation.action['frames'])
            frame_index = int((animation.action['elapsed_time'] // frame_length) % 4)
            animation.frame = animation.action['frames'][frame_index]
            self.change_frame_rect(animation, animation.frame%3, animation.frame//3)
                    
    def draw(self, viewport):
        pass