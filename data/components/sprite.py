from engine.ecs import Component
import pygame
from pygame import Rect

class Sprite(Component):

    def __init__(self, file, frames, columns):
        self.file = file
        self.image = pygame.image.load("resources/" + file)
        self.frames = frames
        self.columns = columns