import pygame
from Img import create_man
from BaseClasses import Object
import Direction as D
import Items

class Player(Object):
    #orect = pygame.Rect(10, 2, 12, 28)
    d=2
    updates = True
    name = "Player"
    isel=0
    cash=0
    def __init__(self, x, y, col, c):
        self.place(x, y)
        self.imgs=create_man(col)
        self.c=c
        self.col=col
        self.inv=[Items.Pickaxe()]
    def update(self, world, events):
        bpress = self.c.get_buttons(events)
        if not self.moving:
            for d in self.c.get_dirs():
                self.d=D.index(d)
                if self.move(d[0], d[1], world):
                    break
            bpressc = self.c.get_pressed()
            if self.inv[self.isel].continuous:
                if bpressc[0]:
                    gos=world.get_os(*D.offset(self.d,self))
                    if gos:
                        self.inv[self.isel].use(gos[0],world)
            if bpress[1]:
                for o in world.get_os(*D.offset(self.d,self)):
                    o.interact(world.w.get_sector(o),self)
        self.isel=(self.isel+bpress[2])%len(self.inv)
    def get_img(self,world):
        return self.imgs[self.d]
    def add_item(self,item):
        if len(self.inv)<7:
            self.inv.append(item)
            return True
    def remove_item(self,item):
        self.inv.remove(item)
        self.isel%=len(self.inv)
