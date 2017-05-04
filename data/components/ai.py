from engine.ecs import Component
from engine.behaviortree import BehaviorTree

class AI(Component):

	def __init__(self, tree_file):

		with open("data/scripts/" + tree_file) as tree_json:
			self.tree = BehaviorTree(tree_json)