
from engine.ecs import Component
import pygame
from pygame import Rect

class Clickable(Component):

    def __init__(self, action):
        self.action = action