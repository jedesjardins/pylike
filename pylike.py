#!/usr/bin/python3

import os, sys
import pygame
from engine.engine import Engine
from engine.state import State
# from engine.ecs import models, managers, exceptions
from engine import Viewport

from data.states import menustate


def main():
    pygame.init()
    
    frame_lock = pygame.time.Clock()
    viewport = Viewport.Viewport()
    
    engine = Engine()
    start_state = menu_state.MenuState()
    engine.push_state(start_state)

    frames_per_second_max = 1
    dt = 1/frames_per_second_max


    while True:
        engine.handle_events()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        engine.update(dt)

        viewport.draw_rect((10, 10, 20, 20))
        viewport.draw()

        engine.draw()

        # TODO(jhives): rework frame time to use dt
        dt = frame_lock.tick(frames_per_second_max)

if __name__ == '__main__':
    main()