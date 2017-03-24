from engine.state import State

class MenuState(State):

	def __init__(self):
		print("\tMenuState, init")
		super().__init__()