
class Viewport():
	""" Translates coordinates from the gamespace to the surface coordinate
		space"""

	def __init__(self, point=(0, 0), size=(800. 600)):
		self.x, self.y = point
		self.w, self.h = size

	def setPosition(self, point=(0, 0)):
		self.x, self.y = point

	def setSize(self, size=(800. 600)):
		self.w, self.h = size

	def draw(self):
		print('unimplemented')

	def draw_rect(self):
		print('unimplemented')

	def center_on(point=(0,0), size=(0,0))
		print('unimplemented')

	def zoom_in(self, percentage):
		print('unimplemented')

	def zoom_out(self, percentage):
		print('unimplemented')

	def translate_rect(self, rect):
		print('unimplemented')

	def on_screen(self, rect):
		print('unimplemented')
