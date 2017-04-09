from engine.ecs import Component
import pygame
from pygame import Rect

class Sprite(Component):

    def __init__(self, file, frames, columns, frame_rect, 
    	edge_buffer={"left": 0, "right": 0, "top": 0, "bottom": 0}):
        self.file = file
        self.image = pygame.image.load("resources/" + file)
        self.frames = frames
        self.columns = columns
        self.frame_rect = Rect(frame_rect["x"], frame_rect["y"], frame_rect["w"], frame_rect["h"])
        self.edge_buffer = edge_buffer
        self.curr_frame_rect = self.frame_rect.copy()