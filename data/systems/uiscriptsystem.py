from engine.ecs import System
from engine.command import Command
import engine.font as Font
from data.components import UIScript, State, Position
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from pygame import Rect
import pygame

import sys

class UIScriptSystem(System):

    class StartScript(Command):
        def __init__(self, e, em, game, p):
            #lock movement of p somehow so the player can't move
            self.script = em.component_for_entity(e, UIScript)
            self.script.target = p
            em.component_for_entity(p, State).locked = True
            em.component_for_entity(p, Position).locked = True


        def do(self):
            if not self.script.running:
                print('Starting script')
                self.script.running = True

    def old_update_text(self, game):
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
            
    def old_draw_text(self, viewport):

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

