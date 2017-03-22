
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
		pass

	def draw_rect(self):
		pass

	def center_on(point=(0,0), size=(0,0))
		pass

	def zoom_in(self, percentage):
		pass

	def zoom_out(self, percentage):
		pass

	def translate_rect(self, rect):
		pass

	def on_screen(self, rect):
		pass
