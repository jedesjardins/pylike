from engine.ecs import Component
import pygame
from pygame import Rect

class Animation(Component):

    def __init__(self, frame_rect, actions):
        self.frame_rect = Rect(frame_rect['x'], frame_rect['y'], frame_rect['w'], frame_rect['h'])
        self.curr_frame_rect = Rect(frame_rect['x'], frame_rect['y'], frame_rect['w'], frame_rect['h'])
        self.actions = actions
        for action, data in self.actions.items():
            data['elapsed_time'] = 0
        self.action = self.actions['down']
        self.frame = self.action['frames'][0]