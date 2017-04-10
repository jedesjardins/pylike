# TODO(jhives): change from keys to actions or something?

from engine.ecs import System
from engine.command import Command
import engine.font as Font
from data.components import MenuOptions
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from pygame import Rect

class MenuSystem(System):

    class Up(Command):
        def __init__(self, e, em, game):
            self.menuoptions = em.component_for_entity(e, MenuOptions)

        def do(self):
            if self.menuoptions.selection > 0:
                self.menuoptions.selection -= 1

    class Down(Command):
        def __init__(self, e, em, game):
            self.menuoptions = em.component_for_entity(e, MenuOptions)

        def do(self):
            if self.menuoptions.selection < len(self.menuoptions.menu_list) - 1:
                self.menuoptions.selection += 1

    class Select(Command):
        def __init__(self, e, em, game):
            self.menuoptions = em.component_for_entity(e, MenuOptions)
            self.game = game

        def do(self):
            menu_selection = self.menuoptions.menu_list[self.menuoptions.selection]
            if menu_selection == 'play':
                self.game['next_state'] = 'PlayState'
            elif menu_selection == 'exit':
                self.game['play_flag'] = False

    def update(self, game):
        pass
        #for e, menuoptions in self.entity_manager.pairs_for_type(MenuOptions):
            #print(menuoptions.title, menuoptions.menu_list)

    def draw(self, viewport):
        for e, menuoptions in self.entity_manager.pairs_for_type(MenuOptions):
            menu_rect = menuoptions.image.get_rect()
            menu_rect.center = viewport.screen.get_rect().center
            viewport.screen.blit(menuoptions.image, menu_rect)

            selection = menuoptions.selection
            arrow = Font.get_text_image('>', 'Minecraft.ttf', 30)
            destx, desty = menuoptions.menu_list_offsets[selection]
            destx -= arrow.get_rect().width
            dest_rect = menu_rect.copy()
            dest_rect.move_ip(destx, desty)
            viewport.screen.blit(arrow, dest_rect)
