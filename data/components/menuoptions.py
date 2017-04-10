
from engine.ecs import Component
import engine.font as Font
import pygame
from pygame import Rect

class MenuOptions(Component):

    def __init__(self, title, menulist={}):
        self.title = title
        self.selection = 0
        self.menu_list = []
        self.menu_list_offsets = []
        for item, action in menulist.items():
            self.menu_list.append(item)

        self.text_images = []
        height = 0
        max_width = 0
        if self.title:
            image = Font.get_text_image('The Menu Bitch', 'Minecraft.ttf', 50)
            self.text_images.append(image)
            rect = image.get_rect()
            height += rect.h
            width = rect.w
            if width > max_width:
                max_width = width
        for option in self.menu_list:
            image = Font.get_text_image(option, 'Minecraft.ttf', 30)
            self.text_images.append(image)
            rect = image.get_rect()
            height += rect.h
            width = rect.w
            if width > max_width:
                max_width = width

        self.image = pygame.Surface((max_width, height))
        self.image.fill((255,255,255))
        y_offset = 0
        index = -1
        for image in self.text_images:
            rect = image.get_rect()
            w, h = rect.size
            x_offset = (max_width-w)//2
            self.image.blit(image, (x_offset, y_offset))
            if index != -1:
                self.menu_list_offsets.append((x_offset, y_offset))
            y_offset += h
            index += 1

        self.text_images = None

        




        