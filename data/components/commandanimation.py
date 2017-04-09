from engine.ecs import Component
import pygame
from pygame import Rect

class CommandAnimation(Component):

    def __init__(self, action_animation):
    	self.action_animation = action_animation
    	self.elapsed_time = 0