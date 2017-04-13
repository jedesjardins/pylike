
from engine.ecs import Component

class Script(Component):

    """ A script wraps a list of actions. Each action is completed before the
        next starts.
        Scripts need to know when an action ends.
        Scripts need to support branching based on menu's 
    """
    
    def __init__(self, actions):
        self.running = True
        self.current_action = 0
        self.actions = actions