from engine.ecs import System
from engine.command import Command
from data.components import Script
from engine.ecs.exceptions import NonexistentComponentTypeForEntity

class ScriptSystem(System):
    
    class StartScript(Command):
        def __init__(self, e, em, game, *_):
            self.script = em.component_for_entity(e, Script)

        def do(self):
            self.script.running = True

    def update(self, game):
        pass