from engine.ecs import Component

class Actions(Component):
    """ Holds a list of (action, status) tuples. ex: ('walk_up', start)
    """
    def __init__(self):
        self.act_list = []