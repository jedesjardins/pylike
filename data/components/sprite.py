from engine.ecs import Component
import pygame
from pygame import Rect

class Sprite(Component):

    def __init__(self, file, rect):
        self.file = file
        self.image = pygame.image.load("resources/" + file)
        self.rect = Rect(rect["x"], rect["y"], rect["w"], rect["h"])