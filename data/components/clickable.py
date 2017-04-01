from engine.ecs import Component

class Clickable(Component):

    def __init__(self, action):
    	self.action = action
