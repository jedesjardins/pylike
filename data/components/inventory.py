from engine.ecs import Component
import pygame

class Inventory(Component):

    def __init__(self, items=[]):
    	self.items = items