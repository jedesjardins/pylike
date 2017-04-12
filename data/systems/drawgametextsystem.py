from engine.ecs import System
from engine.command import Command
from data.components import Textbox
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from pygame import Rect
import pygame

import sys

class DrawGameTextSystem(System):

    class SpawnTextbox(Command):
        def __init__(self, e, em, game, *_):
            self.e = e
            self.em = em

        def do(self):
            self.em.add_component(self.e, Textbox(self.e, 'Hello, my name is urmum, lol'))

        def undo(self):
            pass

    class PrintFullText(Command):
        def __init__(self, e, em, game, *_):
            pass

        def do(self):
            pass

        def undo(self):
            pass

    class EndText(Command):
        def __init__(self, e, em, game, *_):
            pass

        def do(self):
            pass

        def undo(self):
            pass

    def update(self, game):
        cpt = 1000/20
        dt = game['dt']

        for e, textbox in self.entity_manager.pairs_for_type(Textbox):

            if textbox.finished == True:
                continue

            textbox.elapsed_time += dt
            num_chars = int(textbox.elapsed_time//cpt) + 1

            index = num_chars - textbox.total_past_line_length

            #sys.stdout.write(textbox.lines[textbox.last_line][textbox.last_char:index])
            if textbox.last_char != index:
                #sys.stdout.write(textbox.lines[textbox.last_line][textbox.last_char:index])
                textbox.output_buffer[textbox.last_line].append(textbox.lines[textbox.last_line][textbox.last_char:index])
                #sys.stdout.flush()
            textbox.last_char = index

            if index == len(textbox.lines[textbox.last_line]):
                textbox.total_past_line_length = len(textbox.lines[textbox.last_line])
                textbox.last_line += 1
                textbox.last_char = 0
                if textbox.last_line >= len(textbox.lines):
                    print(textbox.output_buffer)
                    textbox.finished = True
                else:
                    textbox.output_buffer.append([])

    def draw(self, viewport):
        square = pygame.Surface((800, 200))
        square.set_alpha(128)
        square.fill((100, 100, 100))
        viewport.screen.blit(square, Rect(0, 400, 800, 200))

        #pygame.draw.rect(viewport.screen, pygame.Color(100, 100, 100, 200), Rect(100, 100, 100, 200))