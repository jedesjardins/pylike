class State(object):

    def __init__(self):
        # print("\tState, init")
        pass

    def enter(self):
        # print("\tState, enter state")
        pass

    def exit(self):
        # print("\tState, exit state")
        pass

    def handle_events(self, keys):
        # print("\tState, handle_events")
        pass

    def update(self, dt):
        # print("\tState, update")
        pass

    def draw(self):
        # print("\tState, draw")
        pass

    def pause(self):
        # print("\tState, pause")
        pass

    def change_state(self, state_manager, state):
        # print("\tState, change state")
        pass