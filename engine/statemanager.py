import pygame
import data.states

class StateManager(object):

    def __init__(self):
        # print('State Manager, init')
        self._running = True
        self._state_stack = []
        self._next_state = None

    def change_state(self, new_state):
        # print('State Manager, change state')
        if self._state_stack:
            self._state_stack[-1].exit()
            self._state_stack.pop()

        self._state_stack.append(new_state)
        self._state_stack[-1].enter()

    def push_state(self, new_state):
        # print('State Manager, push state')
        if self._state_stack:
            self._state_stack[-1].pause()

        self._state_stack.append(new_state)
        self._state_stack[-1].enter()

    def pop_state(self):
        # print('State Manager, pop state')
        if self._state_stack:
            self._state_stack[-1].exit()
            self._state_stack.pop()

        if self._state_stack:
            self._state_stack.resume()

    mouse_map = {1:'leftclick', 2:'rightclick', 3:'middleclick', 4:'scrollup', 5:'scrolldown'}
    ktou = {}
    past_keys = {}

    ascii_to_key = {
        97: 'a',
        98: 'b',
        99: 'c',
        100: 'd',
        101: 'e',
        102: 'f',
        103: 'g',
        104: 'h',
        105: 'i',
        106: 'j',
        107: 'k',
        108: 'l',
        109: 'm',
        110: 'n',
        111: 'o',
        112: 'p',
        113: 'q',
        114: 'r',
        115: 's',
        116: 't',
        117: 'u',
        118: 'v',
        119: 'w',
        120: 'x',
        121: 'y',
        122: 'z',
        273: 'up',
        274: 'down',
        275: 'right',
        276: 'left',
        32: 'space',
        301: 'caps',
        303: 'rshift',
        304: 'lshift',
        306: 'ctrl',
        13: 'enter',
        27: 'esc'
    }

    def update(self, dt):

        keys = {}
        past_keys = self.past_keys
        ktou = self.ktou

        for key, value in past_keys.items():
            if value == 'down' or value == 'held':
                keys[key] = 'held'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
                return

            # maps this key code to the unicode to be stored for keyup
            if event.type == pygame.KEYDOWN:
                # print(event.key)
                if event.key in StateManager.ascii_to_key:
                    keys[StateManager.ascii_to_key[event.key]] = 'down'
                """
                print(event)
                ktou[event.key] = event.unicode
                keys[event.unicode] = 'down'
                """

            # looks into ktou to translate the key code to unicode
            if event.type == pygame.KEYUP:
                if event.key in StateManager.ascii_to_key:
                    keys[StateManager.ascii_to_key[event.key]] = 'up'
                """
                keys[ktou[event.key]] = 'up'
                """

            # TODO(jhives): translate pos to new coordinate system?
            # TODO(jhives): add clickndrag input?
            if event.type == pygame.MOUSEMOTION:
                # also can use rel for relative movement
                # and buttons which is a tuple of what buttons are pressed
                # like (0, 0, 0) or (1, 0, 0)
                keys['mousemove'] = event.pos

            if event.type == pygame.MOUSEBUTTONDOWN:
                keys[StateManager.mouse_map[event.button]] = ('down', event.pos) 

            if event.type == pygame.MOUSEBUTTONUP:
                keys[StateManager.mouse_map[event.button]] = ('up', event.pos)

        self._running, next_state, push_state = self._state_stack[-1].update(dt, keys)

        if next_state:
            state_class = getattr(data.states, next_state)
            self.change_state(state_class())
        elif push_state:
            state_class = getattr(data.states, push_state)
            self.push_state(state_class())

        self.past_keys = keys

    # TODO(jhives): Draw lower states to show the overlay?
    #               Higher states could just not clear the screen to black?
    def draw(self):
        # print('State Manager, draw')
        for state in self._state_stack:
            state.draw()
        self._state_stack[-1].clear()

    @property
    def running(self):
        return self._running