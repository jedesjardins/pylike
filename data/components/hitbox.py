
from engine.ecs import Component
from pygame import Rect

class Hitbox(Component):
    def __init__(self, rect):
        self.rect = Rect(rect["x"], rect["y"], rect["w"], rect["h"])