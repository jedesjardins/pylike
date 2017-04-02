from engine.ecs import Component
import pygame
from pygame import Rect

class Animation(Component):

    def __init__(self, frame_rect, animations):
        self.frame_rect = Rect(frame_rect['x'], frame_rect['y'], frame_rect['w'], frame_rect['h'])
        self.curr_frame_rect = Rect(frame_rect['x'], frame_rect['y'], frame_rect['w'], frame_rect['h'])
        self.animations = animations

        self.elapsed_time = 0
        self.animation = self.animations['down']
        self.frame = self.animation['frames'][0]