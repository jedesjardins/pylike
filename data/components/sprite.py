from engine.ecs import Component
import pygame
from pygame import Rect

class Sprite(Component):

    def __init__(self, file, frames, columns, frame_rect):
        self.file = file
        self.image = pygame.image.load("resources/" + file)
        self.frames = frames
        self.columns = columns
        self.frame_rect = Rect(frame_rect["x"], frame_rect["y"], frame_rect["w"], frame_rect["h"])