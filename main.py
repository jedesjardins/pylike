import os, sys
import pygame
from engine import Viewport
from engine import Actor



def main():
	pygame.init()

	size = (320, 240)
	black = (0, 0, 0)
	screen = pygame.display.set_mode(size)

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

		screen.fill(black)
		pygame.display.flip()

if __name__ == '__main__':
    main()