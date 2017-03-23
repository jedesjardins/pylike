

class Actor(object):
	"""Base class for objects in the game it's an Enitity with components
	   somehow"""
	def __init__(self):
		print("init")

	def update(self):
		print("update")

	def draw(self):
		print("draw")