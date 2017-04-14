from engine.ecs import System
from data.components import State
from engine.command import Command
from engine.ecs.exceptions import NonexistentComponentTypeForEntity

class StateSystem(System):

    class LockDirection(Command):
        def __init__(self, e, em, game):
            self.state = em.component_for_entity(e, State)

        def do(self):
            self.state.lock_direction = True
    
    class Up(Command):
        def __init__(self, e, em, game):
            self.state = em.component_for_entity(e, State)

        def do(self):
            self.state.next_direction.append('up')

    class Down(Command):
        def __init__(self, e, em, game):
            self.state = em.component_for_entity(e, State)

        def do(self):
            self.state.next_direction.append('down')

    class Left(Command):
        def __init__(self, e, em, game):
            self.state = em.component_for_entity(e, State)

        def do(self):
            self.state.next_direction.append('left')

    class Right(Command):
        def __init__(self, e, em, game):
            self.state = em.component_for_entity(e, State)

        def do(self):
            self.state.next_direction.append('right')

    class Run(Command):
        def __init__(self, e, em, game):
            self.state = em.component_for_entity(e, State)

        def do(self):
            pass
            # self.state.next_action.append('run')

    # TODO(jhives): make different attack states, jab, swing, etc
    class Attack(Command):
        def __init__(self, e, em, game):
            self.state = em.component_for_entity(e, State)

        def do(self):
            pass
            # self.state.next_action.append('action')

    def update(self, game):
        for e, state in self.entity_manager.pairs_for_type(State):
            if state.locked:
                continue

            past_action = state.action
            past_direction = state.direction


            state.continue_action = False

            # print(state.next_direction)

            # if no directionals are pressed, change to stand
            if not state.next_direction:
                state.action = 'stand'

            # if a directional is pressed and lock direction is pressed,
            # continue walking
            elif state.lock_direction:
                state.action = 'walk'

            # if a direction is pressed, move in that direction
            else:
                if not state.direction in state.next_direction:
                    state.direction = state.next_direction[0]
                    state.action = 'stand'
                else:
                    state.action = 'walk'

            if past_action == state.action and\
                past_direction == state.direction:
                state.continue_action = True

            # print(state.direction, state.action)

            state.next_direction = []
            state.next_action = []
            state.lock_direction = False