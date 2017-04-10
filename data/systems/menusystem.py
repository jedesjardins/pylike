# TODO(jhives): change from keys to actions or something?

from engine.ecs import System
from engine.command import Command
from data.components import MenuOptions
from engine.ecs.exceptions import NonexistentComponentTypeForEntity

class MenuSystem(System):

    class Up(Command):
        def __init__(self, e, em, game):
            self.menuoptions = em.component_for_entity(e, MenuOptions)

        def do(self):
            if self.menuoptions.selection > 0:
                self.menuoptions.selection -= 1
            print('up', self.menuoptions.selection)

    class Down(Command):
        def __init__(self, e, em, game):
            self.menuoptions = em.component_for_entity(e, MenuOptions)

        def do(self):
            if self.menuoptions.selection < len(self.menuoptions.menulist) - 1:
                self.menuoptions.selection += 1
            print('down', self.menuoptions.selection)

    class Select(Command):
        def __init__(self, e, em, game):
            self.menuoptions = em.component_for_entity(e, MenuOptions)

        def do(self):
            print("Selection: ", 
                self.menuoptions.menulist[self.menuoptions.selection])

    def update(self, game):
        pass
        """
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
        """