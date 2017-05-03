from engine.ecs import Component

class AI(Component):

	def __init__(tree):
		self.tree = tree
		self.curr_node = tree