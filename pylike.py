#!/usr/bin/python3

import os, sys
import pygame
from engine import Viewport
from engine import Actor



def main():
	pygame.init()
	
	frame_lock = pygame.time.Clock()
	viewport = Viewport.Viewport()

	y = 0

	while True:

		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

		viewport.draw_rect((10, y, 20, 20))
		viewport.draw()

		y = y + 1

		# TODO(jhives): rework frame time to use dt
		dt = frame_lock.tick(60)

if __name__ == '__main__':
    main()