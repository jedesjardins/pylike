#!/usr/bin/python3

import os, sys
import pygame
from engine import StateManager
from data.states import *

def main():
    pygame.init()
    
    frame_lock = pygame.time.Clock()
    
    engine = StateManager()
    start_state = PlayState()
    engine.push_state(start_state)

    frames_per_second_max = 10
    dt = 1/frames_per_second_max


    while engine.running:
        engine.update(dt)

        engine.draw()

        # TODO(jhives): rework frame time to use dt
        dt = frame_lock.tick(frames_per_second_max)

    # TODO(jhives): make sure to close any states left open

if __name__ == '__main__':
    main()