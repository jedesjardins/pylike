
from pygame import Rect

class Quadtree(object):

    MAX_DEPTH = 5

    def __init__(self, rect, d=1):
        self.rect = rect
        self.d = d

        self.nodes = {}
        self.entities = []

    def clear(self):
        self.entities = []

        for i, qt in self.nodes.items():
            qt.clear()

        self.nodes = {i:qt for i, qt in self.nodes.items() if not i}

    def split(self):
        rect1 = self.rect.copy()
        rect1.w = rect1.w/2
        rect1.h = rect1.h/2
        self.nodes[1] = Quadtree(rect1, self.d+1)

        rect2 = rect1.copy()
        rect2.x += rect2.w
        self.nodes[2] = Quadtree(rect2, self.d+1)

        rect3 = rect1.copy()
        rect3.y += rect3.h
        self.nodes[3] = Quadtree(rect3, self.d+1)

        rect4 = rect1.copy()
        rect4.x += rect4.w
        rect4.y += rect4.h
        self.nodes[4] = Quadtree(rect4, self.d+1)

    def get_index(self, hitbox):
        index = -1
        x, y, w, h = hitbox.x, hitbox.y, hitbox.w, hitbox.h, 

        vmidpoint = self.rect.x + self.rect.w/2
        hmidpoint = self.rect.y + self.rect.h/2

        topQuad = ((y < hmidpoint) and (y + h < hmidpoint))
        botQuad = y >= hmidpoint

        if ((x < vmidpoint) and (x + w < vmidpoint)):
            if topQuad:
                index = 2
            elif botQuad:
                index = 3
        elif (x >= vmidpoint):
            if topQuad:
                index = 1
            elif botQuad:
                index = 4

        return index

    def insert(self, e, hitbox):
        index = self.get_index(hitbox)
        if index == -1:
            self.entities.append(e)
        else:
            if self.d == Quadtree.MAX_DEPTH:
                self.entities.append(e)
            else:
                if index not in self.nodes:
                    self.split()
                self.nodes[index].insert(e, hitbox)

    def retrieve(self, hitbox):
        index = self.get_index(hitbox)
        neighbors = []

        if index != -1 and index in self.nodes:
            neighbors = self.nodes[index].retrieve(hitbox)
        elif index == -1:
            for i, qt in self.nodes.items():
                neighbors += self.nodes[i].retrieve(hitbox)


        for e in self.entities:
            neighbors.append(e)

        return neighbors



