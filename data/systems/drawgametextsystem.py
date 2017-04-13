from engine.ecs import System
from engine.command import Command
import engine.font as Font
from data.components import Textbox
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from pygame import Rect
import pygame

import sys

class DrawGameTextSystem(System):
    class SpawnInteraction(Command):
        def __init__(self, e, em, game, p):
            self.e = e
            self.p = p
            self.em = em

        def do(self):
            print(self.e)
            self.em.add_component(self.e, Textbox(self.e, "Hey, I'm your doppelganger,#how's it hangin?$We'll just keep going, see#what's happening.. $hum dee dum....$"))


    class SpawnTextbox(Command):
        def __init__(self, e, em, game, *_):
            self.e = e
            self.em = em

        def do(self):
            print(self.e)
            self.em.add_component(self.e, Textbox(self.e, "Hey, I'm your doppelganger,#how's it hangin?$We'll just keep going, see#what's happening.. $hum dee dum....$"))

    class SpeedUpText(Command):
        def __init__(self, e, em, game, *_):
            self.em = em
            self.textbox_list = self.em.pairs_for_type(Textbox)


        def do(self):
            for c, textbox in self.textbox_list:
                if textbox.stop == True:
                    textbox.stop = False
                textbox.speedup = True

    
    def push_next_char(self, textbox, index):
        textbox.changed = True
        c = textbox.lines[textbox.last_line][textbox.last_char:index]
        textbox.output_buffer[textbox.last_line].append(c)
        sys.stdout.write(c)
        sys.stdout.flush()

    def update(self, game):
        dt = game['dt']
        cpt = 1000/12

        e_to_delete = []

        for e, tb in self.entity_manager.pairs_for_type(Textbox):
            if tb.finished:
                continue

            if tb.stop:
                continue

            sdt = dt
            if tb.speedup:
                sdt = 2*dt

            tb.elapsed_time += sdt
            char_index = int(tb.elapsed_time//cpt) + 1

            if char_index > tb.last_char:

                c = tb.text[tb.last_char:char_index]
                line = len(tb.output_buffer)-1

                if '$' in c:
                    # stop
                    # subtract len(c after $) from tb.elapsed_time
                    c_list = c.split('$')
                    tb.output_buffer[line] += c_list[0]
                    tb.output_buffer.append([])
                    sys.stdout.write(c_list[0] + '\n')
                    sys.stdout.flush()
                    tb.last_char = char_index - len(c_list[1])
                    tb.elapsed_time -= cpt*len(c_list[1])
                    tb.stop = True


                elif '#' in c:
                    c_list = c.split('#')

                    for string in c_list:
                        if line == len(tb.output_buffer):
                            tb.output_buffer.append([])
                            sys.stdout.write('\n')

                        tb.output_buffer[line] += string
                        sys.stdout.write(string)
                        sys.stdout.flush()
                        tb.last_char = char_index
                        line += 1

                else:
                    if line == len(tb.output_buffer):
                        tb.output_buffer.append([])
                        sys.stdout.write('\n')

                    sys.stdout.write(c)
                    sys.stdout.flush()
                    tb.output_buffer[line] += c
                    tb.last_char = char_index

                if char_index >= len(tb.text) and not tb.stop:
                    tb.finished = True
                    e_to_delete.append(e)

            tb.speedup = False
        
        for e in e_to_delete:
            self.entity_manager.remove_component(e, Textbox)

    def sdraw(self, viewport):
        pass

    def oldupdate(self, game):
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

            # if it was finished, forget it
            if textbox.finished == True:
                continue

            if textbox.speedup:
                dt = 2*dt

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
            if textbox.finished:
                continue

            textbox.image = pygame.image.load("resources/textbox.png")

            y_offset = 0

            if not textbox.output_buffer[-1]:
                draw_buffer = textbox.output_buffer[-3:]
            else:
                draw_buffer = textbox.output_buffer[-2:]

            for line_array in draw_buffer:
                text = ''.join(line_array)
                text_image = Font.get_text_image(text, 'Minecraft.ttf', 40, (0,0,0))
                textbox.image.blit(text_image, (20, y_offset))
                y_offset += text_image.get_rect().h

            viewport.screen.blit(textbox.image, Rect(0, 460, 800, 140))

