import pygame
from Img import create_man, img4, colswap, sndget
from BaseClasses import Object
import Direction as D
import Items
import Traps
etimes={"Pause":1800,"Slow":900,"Fast":900}
csh=sndget("cash")
nomoney=sndget("nomoney")
class Player(Object):
    #orect = pygame.Rect(10, 2, 12, 28)
    d=2
    updates = True
    name = "Player"
    isel=0
    cash=0
    shop=None
    ssel=0
    scooldown=0
    def __init__(self, x, y, col, c):
        self.place(x, y)
        self.imgs=create_man(col)
        self.c=c
        self.col=col
        self.inv=[Items.Pickaxe(),Items.Defuser(),Items.Trap(Traps.PauseTrap)]
        self.statuseffects=[]
        self.simg=img4("Pointer")
        colswap(self.simg,(255,255,255),col)
    def update(self, world, events):
        bpress = self.c.get_buttons(events)
        pause=False
        self.speed=4
        for se in self.statuseffects[:]:
            if se[1]:
                se[1]-=1
                e=se[0]
                if e=="Pause":
                    pause=True
                if e=="Slow":
                    self.speed=1
                if e=="Fast":
                    self.speed=32
            else:
                self.statuseffects.remove(se)
        if not (self.moving or pause or self.shop):
            for d in self.c.get_dirs():
                self.d=D.index(d)
                if self.move(d[0], d[1], world):
                    break
            bpressc = self.c.get_pressed()
            if self.inv[self.isel].continuous:
                if bpressc[0]:
                    dx,dy=D.offset(self.d,self)
                    gos=world.get_os(*D.offset(self.d,self))
                    self.inv[self.isel].use(gos,world,dx,dy,self)
            else:
                if bpress[0]:
                    dx,dy=D.offset(self.d,self)
                    gos=world.get_os(*D.offset(self.d,self))
                    self.inv[self.isel].use(gos,world,dx,dy,self)
            if bpress[1]:
                for o in world.get_os(*D.offset(self.d,self)):
                    o.interact(world.w.get_sector(o),self)
        elif self.shop:
            if self.scooldown:
                self.scooldown-=1
            else:
                for d in self.c.get_dirs():
                    self.ssel=(self.ssel+d[1])%len(self.shop.items)
                    self.scooldown=15
            if bpress[1]:
                self.shop=None
            if bpress[0]:
                item=self.shop.items[self.ssel]
                if self.cash>=item[1] and self.add_item(Items.wrap(item[0])):
                    self.cash-=item[1]
                    csh.play()
                else:
                    nomoney.play()
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
    def add_effect(self,effect):
        self.statuseffects.append([effect,etimes[effect]])
