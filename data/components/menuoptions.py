
from engine.ecs import Component
import pygame
from pygame import Rect

class MenuOptions(Component):

    def __init__(self, title, menulist):
        self.title = title
        self.selection = 0
        self.menulist = []
        for item, action in menulist.items():
            self.menulist.append(item)

        