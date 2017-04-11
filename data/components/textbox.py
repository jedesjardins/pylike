from engine.ecs import Component
import pygame

class Textbox(Component):

    def __init__(self, parent, text):
        self.parent = parent
        self.text = text
        self.elapsed_time = 0
        self.last_char = 0