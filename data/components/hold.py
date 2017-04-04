from engine.ecs import Component
import pygame

class Hold(Component):

    def __init__(self, hand_locations):
    	self.hand_locations = hand_locations