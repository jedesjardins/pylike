import pygame

"""
self.font = pygame.font.Font("resources/fonts/Minecraft.ttf", 50)
self.text_image = self.font.render("The Menu Bitch", True, (255,255,255))
"""

def make_font(font, size):
	return pygame.font.Font('resources/fonts/{}'.format(font), size)

_cached_fonts = {}
def get_font(font_name, size):
	global _cached_fonts
	key = '{0}|{1}'.format(font_name, str(size))
	font = _cached_fonts.get(key, None)
	if not font:
		font = make_font(font_name, size)
		_cached_fonts[key] = font
	return font

def get_text_image(text, font, size, color=(0,0,0)):
	font = get_font(font, size)
	image = font.render(text, True, color)
	return image