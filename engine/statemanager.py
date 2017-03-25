import pygame

class StateManager(object):

    def __init__(self):
        # print("State Manager, init")
        self._running = True
        self._state_stack = []

    def change_state(self, new_state):
        # print("State Manager, change state")
        if self._state_stack:
            self._state_stack[-1].exit()
            self.pop()

        self._state_stack.append(new_state)
        self._state_stack[-1].enter()

    def push_state(self, new_state):
        # print("State Manager, push state")
        if self._state_stack:
            self._state_stack[-1].pause()

        self._state_stack.append(new_state)
        self._state_stack[-1].enter()

    def pop_state(self):
        # print("State Manager, pop state")
        if self._state_stack:
            self._state_stack[-1].exit()
            self._state_stack.pop()

        if self._state_stack:
            self._state_stack.resume()

    def static_vars(**kwargs):
        def decorate(func):
            for k in kwargs:
                setattr(func, k, kwargs[k])
            return func
        return decorate

    mouse_map = {1:'leftclick', 2:'rightclick', 3:'middleclick', 4:'scrollup', 5:'scrolldown'}

    # static variable ktou maps key code to unicode for easy use in state
    @static_vars(ktou={})
    def handle_events(self):
        # print("State Manager, handle events")
        keys = {}
        ktou = self.handle_events.ktou

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

            # maps this key code to the unicode to be stored for keyup
            if event.type == pygame.KEYDOWN:
                ktou[event.key] = event.unicode
                keys[event.unicode] = "down"

            # looks into ktou to translate the key code to unicode
            if event.type == pygame.KEYUP:
                keys[ktou[event.key]] = "up"

            # TODO(jhives): translate pos to new coordinate system?
            # TODO(jhives): add clickndrag input?
            if event.type == pygame.MOUSEMOTION:
                # also can use rel for relative movement
                # and buttons which is a tuple of what buttons are pressed
                # like (0, 0, 0) or (1, 0, 0)
                keys["mousemove"] = event.pos

            if event.type == pygame.MOUSEBUTTONDOWN:
                keys[Engine.mouse_map[event.button]] = ("down", event.pos) 

            if event.type == pygame.MOUSEBUTTONUP:
                keys[Engine.mouse_map[event.button]] = ("up", event.pos)

        self._running = self._state_stack[-1].handle_events(keys)

    def update(self, dt):
        # print("State Manager, update")
        self._state_stack[-1].update(dt)

    def draw(self):
        # print("State Manager, draw")
        self._state_stack[-1].draw()

    @property
    def running(self):
        return self._running