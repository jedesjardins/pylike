
from engine.ecs import Component
from pygame import Rect

class Hitbox(Component):
    def __init__(self, rect, y_offset):
        self.rect = Rect(rect["x"], rect["y"], rect["w"], rect["h"])
        self.y_offset = y_offset