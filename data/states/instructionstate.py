from engine.state import State
from engine.make import Maker
from engine.viewport import Viewport
from engine.world import World
import engine.font as Font
import engine.ecs as ecs
from data.systems import *
import pygame

class InstructionState(State):

    def __init__(self):
        super().__init__()
        self.text_images = []
        self.text_images.append(Font.get_text_image('Use w,a,s,d to move', 'Minecraft.ttf', 30, (80,66,52)))
        self.text_images.append(Font.get_text_image('Use e to interact', 'Minecraft.ttf', 30, (80,66,52)))
        self.text_images.append(Font.get_text_image('Use enter to operate menus', 'Minecraft.ttf', 30, (80,66,52)))
        self.text_images.append(Font.get_text_image('Use p to pause', 'Minecraft.ttf', 30, (80,66,52)))
        self.text_images.append(Font.get_text_image('Press enter to continue..', 'Minecraft.ttf', 20, (80,66,52)))
        # create viewport
        self.viewport = Viewport()

    def update(self, game):
        keys = game['keys']
        if 'enter' in keys and keys['enter'] == 'down':
            game['state_change'] = [('change', 'MenuState')]

        self.viewport.update()

    def draw(self):
        # self.viewport.screen.blit(self.text_image, (0, 0))

        y_offset = 200

        for image in self.text_images:
            x_offset = (800 - image.get_rect().w)//2
            self.viewport.screen.blit(image, (x_offset, y_offset))
            y_offset += image.get_rect().h
        pass
        

    def clear(self):
        self.viewport.push((222,219,195))