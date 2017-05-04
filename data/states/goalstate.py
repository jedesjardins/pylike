from engine.state import State
from engine.make import Maker
from engine.viewport import Viewport
from engine.world import World
import engine.font as Font
import engine.ecs as ecs
from data.systems import *
import pygame

class GoalState(State):

    def __init__(self):
        super().__init__()
        self.text_images = []
        self.text_images.append(Font.get_text_image('You love your job as a first respond-', 'Minecraft.ttf', 30, (80,66,52)))
        self.text_images.append(Font.get_text_image('er. It prides you to help others.       ', 'Minecraft.ttf', 30, (80,66,52)))
        self.text_images.append(Font.get_text_image('Unfortunately, not everyone can be   ', 'Minecraft.ttf', 30, (80,66,52)))
        self.text_images.append(Font.get_text_image('saved..                                  ', 'Minecraft.ttf', 30, (80,66,52)))
        self.text_images.append(Font.get_text_image('You have been tasked to enter a      ', 'Minecraft.ttf', 30, (80,66,52)))
        self.text_images.append(Font.get_text_image('recently collapsed mine, and save as  ', 'Minecraft.ttf', 30, (80,66,52)))
        self.text_images.append(Font.get_text_image('many of the miners as you can. Just  ', 'Minecraft.ttf', 30, (80,66,52)))
        self.text_images.append(Font.get_text_image("make sure you don't stay too long...    ", 'Minecraft.ttf', 30, (80,66,52)))

        self.text_images.append(Font.get_text_image('Press enter to continue..', 'Minecraft.ttf', 20, (80,66,52)))
        # create viewport
        self.viewport = Viewport()

    def update(self, game):
        keys = game['keys']
        if 'enter' in keys and keys['enter'] == 'down':
            game['state_change'] = [('change', 'PlayState')]

        self.viewport.update()

    def draw(self):
        # self.viewport.screen.blit(self.text_image, (0, 0))

        y_offset = 75

        for image in self.text_images:
            x_offset = (800 - image.get_rect().w)//2
            self.viewport.screen.blit(image, (x_offset, y_offset))
            y_offset += image.get_rect().h
        pass
        

    def clear(self):
        self.viewport.push((222,219,195))