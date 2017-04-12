from engine.ecs import System
from engine.command import Command
import engine.font as Font
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
            self.em.add_component(self.e, Textbox(self.e, "Hey, I'm your doppelganger, how's it hangin? We'll just keep going, see what's happening.. hum dee dum."))

        def undo(self):
            pass

    class FinishText(Command):
        def __init__(self, e, em, game, *_):
            self.em = em
            self.textbox_list = self.em.pairs_for_type(Textbox)


        def do(self):
            for c, textbox in self.textbox_list:
                if textbox.finished:
                    textbox.closed = True
                else:
                    textbox.flush = True

    def update(self, game):
        cpt = 1000/25
        dt = game['dt']


    def draw(self, draw):
        pass

    """
    def push_next_char(self, textbox, index):
        textbox.changed = True
        c = textbox.lines[textbox.last_line][textbox.last_char:index]
        textbox.output_buffer[textbox.last_line].append(c)
        #sys.stdout.write(c)
        #sys.stdout.flush()

    def update(self, game):
        cpt = 1000/25
        dt = game['dt']

        delete = []

        for e, textbox in self.entity_manager.pairs_for_type(Textbox):

            # mark the textbox as not yet changed
            textbox.changed = False

            # if it was closed, delete it
            if textbox.closed:
                delete.append(e)
                continue

            # flush the buffer
            if textbox.flush:
                textbox.output_buffer = []
                for i in range(0, len(textbox.lines)):

                    if i == len(textbox.output_buffer):
                        textbox.output_buffer.append([])

                    textbox.output_buffer[i] = list(textbox.lines[i])

                textbox.flush = False
                textbox.finished = True
                textbox.changed = True

            # if it was finished, forget it
            if textbox.finished == True:
                continue

            # add to the time it was on screen
            textbox.elapsed_time += dt
            # calculate how many characters should be shown
            num_chars = int(textbox.elapsed_time//cpt) + 1


            index = num_chars - textbox.total_past_line_length

            if textbox.last_char != index:
                self.push_next_char(textbox, index)
            textbox.last_char = index

            if index == len(textbox.lines[textbox.last_line]):
                sys.stdout.write('\n')
                sys.stdout.flush()
                textbox.total_past_line_length += len(textbox.lines[textbox.last_line])
                textbox.last_line += 1
                textbox.last_char = 0
                if textbox.last_line >= len(textbox.lines):
                    textbox.finished = True
                else:
                    textbox.output_buffer.append([])

            #('num_chars: {}, index: {}, last_char: {}, line lenth: {}'.\
            #    format(num_chars, index, textbox.last_char, textbox.total_past_line_length))

        for e in delete:
            self.entity_manager.remove_component(e, Textbox)

    def draw(self, viewport):

        for e, textbox in self.entity_manager.pairs_for_type(Textbox):
            if textbox.closed:
                continue

            if textbox.changed:
                textbox.image = pygame.image.load("resources/textbox.png")
                #textbox.image.set_alpha(128)
                #textbox.image.fill((255, 255, 255))
                #textbox.image.set_alpha(255)

                y_offset = 0

                for line_array in textbox.output_buffer[-2:]:
                    text = ''.join(line_array)
                    #print(text)
                    text_image = Font.get_text_image(text, 'Minecraft.ttf', 40, (0,0,0))
                    textbox.image.blit(text_image, (20, y_offset))
                    y_offset += text_image.get_rect().h

                #print()

            viewport.screen.blit(textbox.image, Rect(0, 460, 800, 140))

"""
