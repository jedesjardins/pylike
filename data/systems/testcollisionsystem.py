
# TODO(jhives): change from keys to actions or something?

from engine.ecs import System
from data.components import Position, Hitbox, Commands, Collision, Label, State
from engine.ecs.exceptions import NonexistentComponentTypeForEntity
from data.systems import MovementSystem
from engine.quadtree import Quadtree
from engine.command import Command
from pygame import Rect

def get_hitbox_rect(position, hitbox):
    new_rect = hitbox.rect.copy()
    new_rect.center = position.x, position.y - hitbox.y_offset/2
    return new_rect

class CollisionSystem(System):

    class FloorUp(Command):
        def __init__(self, e, em, game, e2):
            self.world = game['world']

        def do(self):
            if self.world.curr_floor > 0:        
                self.world.curr_floor -= 1

    class FloorDown(Command):
        def __init__(self, e, em, game, e2):
            self.world = game['world']

        def do(self):
            if self.world.curr_floor < self.world.size[2] - 1:
                self.world.curr_floor += 1


    class CollideEntity(Command):
        def __init__(self, e, em, game, e2):
            self.commands = em.component_for_entity(e, Commands)
            print(e, e2)

        def do(self):        
            for command in self.commands.past_commands:
                command.undo()

        def undo(self):
            for command in self.commands.past_commands:
                command.do()

    class CollideWorld(Command):
        def __init__(self, e, em, game, *_):
            self.commands = em.component_for_entity(e, Commands)
            directions, *_ = _

            self.direction_classes = []
            for direction in directions:
                if direction == 'left':
                    self.direction_classes.append(MovementSystem.MoveLeft)
                elif direction == 'right':
                    self.direction_classes.append(MovementSystem.MoveRight)
                elif direction == 'up':
                    self.direction_classes.append(MovementSystem.MoveUp)
                elif direction == 'down':
                    self.direction_classes.append(MovementSystem.MoveDown)

        def do(self):
            for command in self.commands.past_commands:
                if type(command) in self.direction_classes:
                    command.undo()

        def undo(self):
            for command in self.commands.past_commands:
                command.do()

    class CollideWorld2(Command):
        def __init__(self, e, em, game, *_):
            self.commands = em.component_for_entity(e, Commands)

            if _[0] == 'left':
                self.direction_class = MovementSystem.MoveLeft
            elif _[0] == 'right':
                self.direction_class = MovementSystem.MoveRight
            elif _[0] == 'up':
                self.direction_class = MovementSystem.MoveUp
            elif _[0] == 'down':
                self.direction_class = MovementSystem.MoveDown

        def do(self):
            print(self.direction_class)
            for command in self.commands.past_commands:
                if type(command) == self.direction_class:
                    command.undo()

        def undo(self):
            for command in self.commands.past_commands:
                command.do()

    class Push(Command):
        def __init__(self, e, em, game, e2):
            self.e_position = em.component_for_entity(e, Position)
            self.e_hitbox = em.component_for_entity(e, Hitbox)
            self.e2_position = em.component_for_entity(e2, Position)
            self.e2_hitbox = em.component_for_entity(e2, Hitbox)
            self.e2_state = em.component_for_entity(e2, State)

        def do(self):
            ex, ey = self.e_position.x, self.e_position.y
            e2x, e2y = self.e2_position.x, self.e2_position.y

            pushy = abs(e2x-ex)<abs(e2y-ey)

            # TODO(jhives): Stop using state here
            if pushy:
                if ey > e2y and self.e2_state.direction != 'down':
                    rect_e = get_hitbox_rect(self.e_position, self.e_hitbox)
                    rect_e2 = get_hitbox_rect(self.e2_position, self.e2_hitbox)

                    delta_y = (e2y+(rect_e2.h/2)) - (ey-(rect_e.h/2))
                    self.e_position.y += delta_y
                elif ey < e2y and self.e2_state.direction != 'up':
                    # push e down
                    rect_e = get_hitbox_rect(self.e_position, self.e_hitbox)
                    rect_e2 = get_hitbox_rect(self.e2_position, self.e2_hitbox)

                    delta_y = (ey+(rect_e.h/2)) - (e2y-(rect_e2.h/2))  
                    self.e_position.y -= delta_y

            else: 
                if ex > e2x and self.e2_state.direction != 'left':
                    # push e right
                    rect_e = get_hitbox_rect(self.e_position, self.e_hitbox)
                    rect_e2 = get_hitbox_rect(self.e2_position, self.e2_hitbox)

                    delta_x = (e2x+(rect_e2.w/2)) - (ex-(rect_e.w/2))
                    self.e_position.x += delta_x
                elif ex < e2x and self.e2_state.direction != 'right':
                    # push e left
                    rect_e = get_hitbox_rect(self.e_position, self.e_hitbox)
                    rect_e2 = get_hitbox_rect(self.e2_position, self.e2_hitbox)

                    delta_x = (ex+(rect_e.w/2)) - (e2x-(rect_e2.w/2)) 
                    self.e_position.x -= delta_x

    def entity_collisions(self, game):
        dt = game['dt']
        keys = game['keys']
        qt = Quadtree(Rect(0, 0, 100, 100))
        entities = []

        # fill quadtree
        for e, hitbox in self.entity_manager.pairs_for_type(Hitbox):
            try:
                position = self.entity_manager.component_for_entity(e, Position)
            except NonexistentComponentTypeForEntity:
                continue

            # put all hitboxes centered on position into the quadtree as 
            # TODO: How do I get the screen dimensions? Maybe pass game datastructure?

            entities.append(e)
            qt.insert(e, get_hitbox_rect(position, hitbox))


        # iterate all objects and resolve collisions
        for e in entities:
            hitbox = self.entity_manager.component_for_entity(e, Hitbox)
            position = self.entity_manager.component_for_entity(e, Position)

            hb = get_hitbox_rect(position, hitbox)

            try:
                collision = self.entity_manager.component_for_entity(e, Collision)
            except NonexistentComponentTypeForEntity:
                collision = None

            for c in qt.retrieve(hb):
                chitbox = self.entity_manager.component_for_entity(c, Hitbox)
                cposition = self.entity_manager.component_for_entity(c, Position)
                chb = get_hitbox_rect(cposition, chitbox)

                try:
                    label = self.entity_manager.component_for_entity(c, Label).label
                except NonexistentComponentTypeForEntity:
                    label = ''

                if e != c and hb.colliderect(chb) and collision:
                    if label in collision.type_commands:
                        print(e, c)
                        for command in collision.type_commands[label]:
                            d = command(e, self.entity_manager, game, c)
                            d.do()

    def world_collision(self, game):
        dt = game['dt']
        keys = game['keys']
        world = game['world']

        for e, hitbox in self.entity_manager.pairs_for_type(Hitbox):
            try:
                position = self.entity_manager.component_for_entity(e, Position)
            except NonexistentComponentTypeForEntity:
                continue

            try:
                collision = self.entity_manager.component_for_entity(e, Collision)
            except NonexistentComponentTypeForEntity:
                collision = None

            hb = hitbox.rect.copy()
            hb.center = position.x, position.y - hitbox.y_offset/2

            collide_tiles = world.get_collision(hb)
            player_tile = world.point_to_tile((position.x, position.y))

            if collide_tiles and collision:

                collide_directions = []
                
                for collide_tile in collide_tiles:
                    if 'world' in collision.type_commands:
                        dx = player_tile[0] - collide_tile[0]
                        dy = player_tile[1] - collide_tile[1]
                        collide_point = world.tile_to_point(collide_tile)

                        dxp = position.x - collide_point[0]
                        dyp = position.y - collide_point[1]

                        if abs(dyp) > abs(dxp):
                            # vertical collision
                            if dyp > 0:
                                collide_directions.append('down')
                            elif dyp < 0:
                                collide_directions.append('up')
                        else:
                            # horizontal collision
                            if dxp > 0:
                                collide_directions.append('left')
                            elif dxp < 0:
                                collide_directions.append('right')

                    if 'world' in collision.type_commands:
                        for command in collision.type_commands['world']:
                            c = command(e, self.entity_manager, game, collide_directions)
                            c.do()

    def get_pos_hit_col_lab(self, e):
        try:
            position = self.entity_manager.component_for_entity(e, Position)
        except NonexistentComponentTypeForEntity:
            position = None
        try:
            hitbox = self.entity_manager.component_for_entity(e, Hitbox)
        except NonexistentComponentTypeForEntity:
            hitbox = None
        try:
            collision = self.entity_manager.component_for_entity(e, Collision)
        except NonexistentComponentTypeForEntity:
            collision = None
        try:
            label = self.entity_manager.component_for_entity(e, Label)
        except NonexistentComponentTypeForEntity:
            label = None
        return (position, hitbox, collision, label)

    def collisions(self, game):
        keys = game['keys']
        qt = Quadtree(Rect(0, 0, 100, 100))
        entities = []

        # fill quadtree
        for e, hitbox in self.entity_manager.pairs_for_type(Hitbox):
            try:
                position = self.entity_manager.component_for_entity(e, Position)
            except NonexistentComponentTypeForEntity:
                continue

            # put all hitboxes centered on position into the quadtree as 
            # TODO: How do I get the screen dimensions? Maybe pass game datastructure?

            entities.append(e)
            qt.insert(e, get_hitbox_rect(position, hitbox))

        # iterate all objects and resolve collisions
        for e in entities:

            position, hitbox, collision, label = self.get_pos_hit_col_lab(e)
            if not position or not hitbox or not collision or not label:
                continue

            hb = get_hitbox_rect(position, hitbox)
            

            for c in qt.retrieve(hb):
                cposition, chitbox, ccollision, clabel = self.get_pos_hit_col_lab(c)

                if not cposition or not chitbox:
                    continue

                chb = get_hitbox_rect(cposition, chitbox)

                if e != c and hb.colliderect(chb):
                    # resolve e
                    if collision and clabel and clabel.label in collision.type_commands:
                        for command in collision.type_commands[clabel.label]:
                            d = command(e, self.entity_manager, game, c)
                            d.do()

                    # resolve c
                    if ccollision and label and label.label in ccollision.type_commands:
                        for command in ccollision.type_commands[label.label]:
                            d = command(c, self.entity_manager, game, e)
                            d.do()

    def update(self, game):
        self.collisions(game)

        """
        self.entity_collisions(game)

        if 'world' in game:
            self.world_collision(game)
        """