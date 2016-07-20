import pygame
from Img import create_man, img4, colswap, sndget, create_sinking_man
from BaseClasses import Object
import Direction as D
import Items
import Objects
etimes={"Pause":1800,"Slow":900,"Fast":900,"Reverse":1800}
csh=sndget("cash")
nomoney=sndget("nomoney")
pdie=sndget("pdie")
class Player(Object):
    orect = pygame.Rect(20, 4, 24, 56)
    d=2
    updates = True
    name = "Player"
    isel=0
    cash=0
    shop=None
    ssel=0
    scooldown=0
    dead=False
    defaultspeed=4
    sinking=0
    def __init__(self, x, y, col, c):
        self.place(x, y)
        self.imgs=create_man(col)
        self.sinkimgs=create_sinking_man(col)
        self.c=c
        self.col=col
        stbombs=Items.StackPlacer(Objects.Bomb)
        stbombs.stack=3
        self.inv=[Items.Pickaxe(),Items.Defuser(),stbombs]
        self.statuseffects=[]
        self.simg=img4("Pointer")
        self.rerect()
        colswap(self.simg,(255,255,255),col)
    def update(self, world, events):
        bpress = self.c.get_buttons(events)
        pause=False
        self.speed=self.defaultspeed
        reverse=False
        for se in self.statuseffects[:]:
            if se[1]:
                se[1]-=1
                e=se[0]
                if e=="Pause":
                    pause=True
                if e=="Slow":
                    self.speed=1
                if e=="Fast":
                    self.speed=16
                if e=="Reverse":
                    reverse=True
            else:
                self.statuseffects.remove(se)
        if not (self.moving or pause or self.shop or self.sinking):
            bpressc = self.c.get_pressed()
            for d in self.c.get_dirs():
                self.d=D.index(d)
                if reverse:
                    d=D.anti(d)
                if not bpressc[1] and self.move(d[0], d[1], world):
                    break
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
        elif self.sinking:
            self.sinking+=1
            if self.sinking==57:
                self.die(world)
                self.sinking=0
        self.isel=(self.isel+bpress[2])%len(self.inv)
    def get_img(self,world):
        if self.sinking:
            return self.sinkimgs[(self.sinking-1)//4]
        return self.imgs[self.d]
    def add_item(self,item):
        if item.name=="Upgrade":
            return item.upgrade(self)
        else:
            if item.stack:
                for i in self.inv:
                    if i.name==item.name and i.stack<10:
                        i.stack+=1
                        return True
            if len(self.inv)<7:
                self.inv.append(item)
                return True
    def remove_item(self,item):
        self.inv.remove(item)
        self.isel%=len(self.inv)
    def add_effect(self,effect):
        self.statuseffects.append([effect,etimes[effect]])
    def die(self,world):
        if not any([i.name=="Shield" for i in self.inv]):
            stbombs=Items.StackPlacer(Objects.Bomb)
            stbombs.stack=3
            self.inv=[Items.Pickaxe(),Items.Defuser(),stbombs]
            self.defaultspeed=4
        else:
            for i in self.inv:
                if i.name=="Shield":
                    self.inv.remove(i)
                    break
        self.dead=1800
        self.isel%=len(self.inv)
        world.dest(self)
        pdie.play()
