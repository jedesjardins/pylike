from engine.ecs import System
from engine.command import Command
from data.components import Textbox
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from pygame import Rect

import sys

class DrawGameTextSystem(System):

    class SpawnTextbox(Command):
        def __init__(self, e, em, game, *_):
            self.e = e
            self.em = em

        def do(self):        
            print("Creating textbox")
            self.em.add_component(self.e, Textbox(self.e, 'Hello, my name is ur mum, lol\n'))

        def undo(self):
            pass

    def update(self, game):
        lpt = 1000/15
        dt = game['dt']

        for e, textbox in self.entity_manager.pairs_for_type(Textbox):
            textbox.elapsed_time += dt
            num_chars = int(textbox.elapsed_time//lpt) + 1
            if num_chars <= len(textbox.text):
                sys.stdout.write(textbox.text[textbox.last_char:num_chars])
                sys.stdout.flush()
            textbox.last_char = num_chars


    def draw(self, viewport):
        # draw text
        pass