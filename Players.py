import pygame
from Img import create_man, imgx, colswap, sndget, create_sinking_man
from BaseClasses import Object
import Direction as D
import Items
import Objects
import DeathGame
etimes={"Pause":300,"Slow":900,"Fast":900,"Reverse":1800}
csh=sndget("cash")
nomoney=sndget("nomoney")
pdie=sndget("pdie")
teammoney=[0,0]
class Player(Object):
    orect = pygame.Rect(20, 4, 24, 56)
    d=2
    updates = True
    name = "Player"
    isel=0
    _cash=0
    shop=None
    ssel=0
    scooldown=0
    dead=False
    defaultspeed=4
    sinking=0
    iinv=None
    rumbling=0
    dt=0
    def __init__(self, x, y, col, c, gm, team=None):
        self.place(x, y)
        self.imgs=create_man(col)
        self.sinkimgs=create_sinking_man(col)
        self.c=c
        self.col=col
        self.gm=gm
        self.inv=self.gm.create_inv()
        self.statuseffects=[]
        self.simg=imgx("Pointer")
        self.rerect()
        self.team=team
        colswap(self.simg,(255,255,255),col)
    def update(self, world, events):
        bpress = self.c.get_buttons(events)
        pause=False
        self.speed=self.defaultspeed
        reverse=False
        if self.rumbling:
            self.rumbling-=1
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
        if not (self.strafing or pause or self.shop or self.sinking):
            bpressc = self.c.get_pressed()
            if self.iinv:
                item = self.iinv.inv[self.isel]
            else:
                item = self.inv[self.isel]
            if item.continuous:
                if bpressc[0]:
                    dx,dy=D.offset(self.d,self)
                    gos=world.get_os(*D.offset(self.d,self))
                    item.use(gos,world,dx,dy,self)
            else:
                if bpress[0]:
                    dx,dy=D.offset(self.d,self)
                    gos=world.get_os(*D.offset(self.d,self))
                    if item.inv:
                        self.iinv=item
                        self.isel%=len(item.inv)
                    else:
                        item.use(gos,world,dx,dy,self)
        if not (self.moving or pause or self.shop or self.sinking):
            for d in self.c.get_dirs():
                self.d=D.index(d)
                if reverse:
                    d=D.anti(d)
                if not bpressc[1] and self.move(d[0], d[1], world):
                    break
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
        rs=self.c.get_rstick()
        if rs!=(0,0):
            self.d=D.index(rs)
    def get_img(self,world):
        if self.sinking:
            return self.sinkimgs[(self.sinking-1)//4]
        return self.imgs[self.d]
    def add_item(self,item):
        if item.name=="Upgrade":
            return item.upgrade(self)
        else:
            invs=[]
            for i in self.inv:
                if i.inv and i.add_item(item):
                    invs.append(i.inv)
            invs.append(self.inv)
            for inv in invs:
                if item.stack:
                    for i in inv:
                        if i.name==item.name and i.stack<10:
                            i.stack+=1
                            return True
                if len(inv)<7:
                    inv.append(item)
                    return True
    def remove_item(self,item):
        for i in self.inv[:]:
            if i is item:
                self.inv.remove(i)
                break
            elif i.inv:
                if item in i.inv:
                    i.inv.remove(item)
                    break
        if self.iinv:
            self.isel%=len(self.iinv.inv)
        else:
            self.isel%=len(self.inv)
    def add_effect(self,effect,time=None):
        self.statuseffects.append([effect,etimes[effect] if time is None else time])
    def die(self,world):
        if not any([i.name=="Shield" for i in self.inv]):
            for i in self.inv:
                i.on_destroy()
            self.inv=self.gm.create_inv()
            self.defaultspeed=4
        else:
            for i in self.inv:
                if i.name=="Shield":
                    self.inv.remove(i)
                    break
        self.dead=DeathGame.DeathGame(self)
        self.dt=10
        self.isel%=len(self.inv)
        world.dest(self)
        pdie.play()
        self.shop=None
        self.rumbling=0
        self.xoff,self.yoff=0,0
    def get_all_items(self):
        allinvs= [self.inv]+[i.inv for i in self.inv if i.inv]
        return [item for inv in allinvs for item in inv]
    def emp(self,world):
        self.add_effect("Slow")
    @property
    def cash(self):
        if self.team is None:
            return self._cash
        return teammoney[self.team]
    @cash.setter
    def cash(self,value):
        if self.team is None:
            self._cash=value
        else:
            teammoney[self.team]=value
    @property
    def strafing(self):
        return self.moving and D.get_dir(self.d)!=(self.dx,self.dy)
