
import json, sys

class Blackboard:

	_data = {}

	def store(node_path, data):
		_data[node_path] = data

	def fetch(node_path):
		if _data[node_path]:
			return _data[node_path]

class Node():

	_status = None

	def __init__(self, name):
		self.name = name

	def update(self, game, e):
		pass

class Composite(Node):
	pass

class Sequence(Composite):
	pass

class Parallel(Composite):
	pass

class Selector(Composite):
	pass

class RandSelector(Composite):
	pass

class Decorator(Node):
	pass

class Leaf(Node):
	pass

# This is where the real functionality goes
class Action(Leaf):
	pass

class BehaviorTree():

	def __init__(self, tree_json):
		self.tree = json.loads(tree_json)
		self.nodes = {}
		self.prepare_nodes(self.tree)
		self.node_stack = []

	def load(self, tree_json):
		self.tree = json.loads(tree_file)
		self.prepare_nodes(self.tree)

	def prepare_nodes(self, node):
		if not node:
			return

		print(node['name'])

		module = sys.modules[__name__]

		self.nodes[node['name']] = {}
		self.nodes[node['name']]['config'] = node
		
		class_ = getattr(module, node['class'])
		self.nodes[node['name']]['node'] = class_(node['name'])

		for node_child in node["children"]:
			self.prepare_nodes(node_child)

	def update(self, game):
		pass
