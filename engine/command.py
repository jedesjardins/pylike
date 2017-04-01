class Command(object):

	def __init__(self):
		pass

	def do(self):
		print("do", self.value)

	def undo(self):
		print("undo", self.value)

