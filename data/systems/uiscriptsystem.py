from engine.ecs import System
from engine.command import Command
import engine.font as Font
from data.components import UIScript, State, Position
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from pygame import Rect
import pygame
import sys
from copy import deepcopy

class UIScriptSystem(System):

    class UISelect(Command):
        def __init__(self, e, em, game, *_):
            self.em = em
            self.script_list = self.em.pairs_for_type(UIScript)


        def do(self):
            for c, script in self.script_list:
                if script.info['stop']:
                    script.info['stop'] = False
                script.info['selected'] = True

    class UISpeedup(Command):
        def __init__(self, e, em, game, *_):
            self.em = em
            self.script_list = self.em.pairs_for_type(UIScript)


        def do(self):
            for c, script in self.script_list:
                script.info['speedup'] = True

    class UIUp(Command):
        def __init__(self, e, em, game, *_):
            self.em = em
            self.script_list = self.em.pairs_for_type(UIScript)


        def do(self):
            for c, script in self.script_list:
                if script.running:
                    if script.info['selection'] != 0:
                        script.info['selection'] -= 1

    class UIDown(Command):
        def __init__(self, e, em, game, *_):
            self.em = em
            self.script_list = self.em.pairs_for_type(UIScript)


        def do(self):
            for c, script in self.script_list:
                if script.running:
                    options = script.blocks[script.curr_block][script.curr_line][2]

                    if script.info['selection'] != len(options)-1:
                        script.info['selection'] += 1

    class Lock(Command):
        def __init__(self, e, em, game, *_):
            self.state = em.component_for_entity(e, State)
            self.position = em.component_for_entity(e, Position)

        def do(self):
            self.state.locked = True
            self.position.locked = True

        def undo(self):
            self.state.locked = False
            self.position.locked = False

    class StartScript(Command):
        def __init__(self, e, em, game, p):
            #lock movement of p somehow so the player can't move
            self.script = em.component_for_entity(e, UIScript)
            self.script.target = p

            self.script.lock = UIScriptSystem.Lock(p, em, game, e)

        def do(self):
            if not self.script.running:
                self.script.lock.do()
                self.script.info = deepcopy(UIScript.info)
                self.script.curr_block = 'enter'
                self.script.curr_line = 0
                self.script.running = True

    def update_text(self, game, script):
        dt = game['dt']
        cpt = 1000/12
        info = script.info
        text = script.blocks[script.curr_block][script.curr_line][1]

        if info['finished']:
            print("Text shouldn't be finished..")

        if info['stop']:
            return

        sdt = dt
        if info['speedup']:
            sdt = 2*dt

        info['elapsed_time'] += sdt
        char_index = int(info['elapsed_time']//cpt) + 1

        if char_index > info['last_char']:

            c = text[info['last_char']:char_index]
            line = len(info['output_buffer'])-1

            if '$' in c:
                # stop
                # subtract len(c after $) from tb.elapsed_time
                c_list = c.split('$')
                info['output_buffer'][line] += c_list[0]
                info['output_buffer'].append([])
                sys.stdout.write(c_list[0] + '\n')
                sys.stdout.flush()
                info['last_char'] = char_index - len(c_list[1])
                info['elapsed_time'] -= cpt*len(c_list[1])
                info['stop'] = True


            elif '#' in c:
                c_list = c.split('#')

                for string in c_list:
                    if line == len(info['output_buffer']):
                        info['output_buffer'].append([])
                        sys.stdout.write('\n')

                    info['output_buffer'][line] += string
                    sys.stdout.write(string)
                    sys.stdout.flush()
                    info['last_char'] = char_index
                    line += 1

            else:
                if line == len(info['output_buffer']):
                    info['output_buffer'].append([])
                    sys.stdout.write('\n')

                sys.stdout.write(c)
                sys.stdout.flush()
                info['output_buffer'][line] += c
                info['last_char'] = char_index

        if char_index >= len(text) and not info['stop']:
            info['finished'] = True

        info['speedup'] = False

    def update_menu(self, game, script):
        self.update_text(game, script)

        if script.info['finished']:
            script.info['finished'] = False

            if script.info['selected']:
                script.info['finished'] = True

                options = script.blocks[script.curr_block][script.curr_line][2]

                script.info['next_block'] = options[script.info['selection']][1]
        else:
            script.info['selected'] = False

    def set_flags(self, game, script, val=True):
        flags = script.blocks[script.curr_block][script.curr_line][1]

        for flag in flags:
            game['flags'][flag] = val


        script.info['finished'] = True

    def unset_flags(self, game, script):
        self.set_flags(game, script, False)

    def check_flags(self, game, script):
        info = script.info
        command = script.blocks[script.curr_block][script.curr_line]
        flag = command[1]

        if flag in game['flags'] and game['flags'][flag]:
            info['next_block'] = command[2]
        else:
            info['next_block'] = command[3]

        info['finished'] = True

    def update(self, game):
        for e, script in self.entity_manager.pairs_for_type(UIScript):
            if not script.running:
                continue

            curr_type = script.blocks[script.curr_block][script.curr_line][0]

            if curr_type == 'text':
                self.update_text(game, script)
            elif curr_type == 'menu':
                self.update_menu(game, script)
            elif curr_type == 'setflag':
                self.set_flags(game, script)
            elif curr_type == 'unsetflag':
                self.unset_flags(game, script)
            elif curr_type == 'checkflag':
                self.check_flags(game, script)

            else:
                print('unchecked: ', script.blocks[script.curr_block][script.curr_line])
            if script.info['finished']:
                script.curr_line += 1

                if script.info['next_block']:
                    script.curr_block = script.info['next_block']
                    script.curr_line = 0

                script.info = deepcopy(UIScript.info)

            if script.curr_line == len(script.blocks[script.curr_block]):
                script.running = False
                script.lock.undo()

    def display_text(self, viewport, script):
        if script.info['finished']:
            return

        textbox_image = pygame.image.load("resources/textbox.png")

        y_offset = 0

        if not script.info['output_buffer'][-1]:
            draw_buffer = script.info['output_buffer'][-3:]
        else:
            draw_buffer = script.info['output_buffer'][-2:]

        for line_array in draw_buffer:
            text = ''.join(line_array)
            text_image = Font.get_text_image(text, 'Minecraft.ttf', 40, (80,66,52))
            textbox_image.blit(text_image, (20, y_offset))
            y_offset += text_image.get_rect().h

        if script.info['stop']:
            if not 'down_arrow' in script.info:
                script.info['down_arrow'] = pygame.image.load("resources/down_arrow.png")
            textbox_image.blit(script.info['down_arrow'], (755, 115))

        viewport.screen.blit(textbox_image, Rect(0, 460, 800, 140))

    def display_menu(self, viewport, script):
        if script.info['finished']:
            return

        self.display_text(viewport, script)
        
        options = script.blocks[script.curr_block][script.curr_line][2]

        option_images = []

        total_height = 0
        max_width = 0

        for option in options:
            text_image = Font.get_text_image(option[0], 'Minecraft.ttf', 40, (80,66,52))
            total_height += text_image.get_rect().h

            if text_image.get_rect().w > max_width:
                max_width = text_image.get_rect().w

            option_images.append(text_image)

        x_pos = 800 - max_width - 40
        y_pos = 460 - total_height - 20

        options_image = pygame.Surface((max_width+40, total_height+20))
        options_image.fill((222,219,195))

        y_offset = 0

        i = 0
        arrow_y = 0
        for image in option_images:
            if i == script.info['selection']:
                arrow_y = y_offset 
            options_image.blit(image, (25, y_offset))
            y_offset += image.get_rect().h
            i += 1

        if not 'right_arrow' in script.info:
            script.info['right_arrow'] = pygame.image.load("resources/right_arrow.png")
        options_image.blit(script.info['right_arrow'], (5, arrow_y+20))

        viewport.screen.blit(options_image, Rect(x_pos, y_pos, 800, 140))

    def draw(self, viewport):
        for e, script in self.entity_manager.pairs_for_type(UIScript):
            if not script.running:
                continue

            curr_type = script.blocks[script.curr_block][script.curr_line][0]

            if curr_type == 'text':
                self.display_text(viewport, script)
            elif curr_type == 'menu':
                self.display_menu(viewport, script)

