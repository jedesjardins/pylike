#!/usr/bin/python3

import os, sys
import pygame
from engine.engine import Engine
from engine.state import State
# from engine.ecs import models, managers, exceptions
# from engine import Viewport

from data.states import menustate


def main():
    pygame.init()
    
    frame_lock = pygame.time.Clock()
    
    engine = Engine()
    start_state = menustate.MenuState()
    engine.push_state(start_state)

    frames_per_second_max = 30
    dt = 1/frames_per_second_max


    while engine.running:
        engine.handle_events()

        engine.update(dt)

        engine.draw()

        # TODO(jhives): rework frame time to use dt
        dt = frame_lock.tick(frames_per_second_max)

    # TODO(jhives): make sure to close any states left open

if __name__ == '__main__':
    main()