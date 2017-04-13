from engine.ecs import Component
import pygame

class Textbox(Component):

    def __init__(self, parent, text, max_length=30):
        self.parent = parent
        self.text = text

        self.elapsed_time = 0
        self.last_char = 0

        self.output_buffer = [[]]
        self.finished = False
        self.speedup = False
        self.stop = False