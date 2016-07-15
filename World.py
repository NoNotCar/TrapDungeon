import Tiles
import Objects
import pygame
from random import randint
import Img
import Players
cashfont=Img.fload("cool",32)
class World(object):
    m=5
    def __init__(self,ps):
        hs=HomeSector(self,0,0,ps)
        self.ps=ps
        self.w={(0,0):hs}
    def update(self,events):
        for s in self.w.itervalues():
            s.update(events)
    def render(self,p,screen):
        asx=p.x*64+int(round(p.xoff))-192
        asy=p.y*64+int(round(p.yoff))-256
        sx=p.x
        sy=p.y
        for y in range(sy-self.m,sy+self.m+2):
            for x in range(sx-self.m,sx+self.m+1):
                screen.blit(Tiles.tiles[self.get_t(x,y)].get_img(),(x*64-asx,y*64-asy))
        for y in range(sy-self.m,sy+self.m+2):
            for x in range(sx-self.m,sx+self.m+1):
                objs=self.get_os(x,y)
                for o in objs:
                    screen.blit(o.get_img(self),(x*64+o.xoff-asx,y*64+o.yoff-asy-o.o3d*4))
        pygame.draw.rect(screen,p.col,pygame.Rect(0,64,448,452),2)
        pygame.draw.rect(screen,(200,200,200),pygame.Rect(0,0,448,64))
        for n,i in enumerate(p.inv):
            screen.blit(i.get_img(),(n*64,0))
            if n==p.isel:
                pygame.draw.rect(screen,p.col,pygame.Rect(n*64,60,64,4))
        Img.bcentrex(cashfont,str(p.cash),screen,468,(255,255,0))
        if p.statuseffects:
            maxt=max([se[1] for se in p.statuseffects])
            maxse=[se for se in p.statuseffects if se[1]==maxt][0]
            pygame.draw.rect(screen,p.col,pygame.Rect(0,507,maxt*448//Players.etimes[maxse[0]],12))
    def get_t(self,x,y):
        sx=x//16
        sy=y//16
        try:
            return self.w[(sx,sy)].get_t(x,y)
        except KeyError:
            self.new_sector(sx,sy)
            return self.get_t(x,y)
    def get_os(self,x,y):
        sx=x//16
        sy=y//16
        try:
            return self.w[(sx,sy)].get_os(x,y)
        except KeyError:
            self.new_sector(sx,sy)
            return self.get_t(x,y)
    def new_sector(self,sx,sy):
        self.w[(sx,sy)]=Sector(self,sx,sy)
    def is_clear(self,x,y):
        sx=x//16
        sy=y//16
        try:
            return self.w[(sx,sy)].is_clear(x,y)
        except KeyError:
            self.new_sector(sx,sy)
            return self.is_clear(x,y)
    def spawn(self,o):
        sx=o.x//16
        sy=o.y//16
        try:
            self.w[(sx,sy)].spawn(o)
        except KeyError:
            self.new_sector(sx,sy)
            self.spawn(o)
    def get_sector(self,o):
        sx=o.x//16
        sy=o.y//16
        try:
            return self.w[(sx,sy)]
        except KeyError:
            self.new_sector(sx,sy)
            return self.get_sector(o)
class Sector(object):
    def __init__(self,w,x,y):
        self.x=x
        self.y=y
        self.t=[[0]*16 for n in range(16)]
        self.o=[[None]*16 for n in range(16)]
        self.size=(16,16)
        self.oconvert()
        self.build()
        self.w=w
    def build(self):
        for x in range(16):
            for y in range(16):
                if not randint(0,100):
                    self.spawnX(Objects.Diamond(x,y))
                elif randint(0,1):
                    self.spawnX(Objects.Wall(x,y))
    def oconvert(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.o[x][y]=[]
        self.uos=[]
    def update(self,events):
        for o in self.uos:
            o.update(self,events)
            o.mupdate(self)
    def spawn(self,o):
        x,y=self.d_pos(o.x,o.y)
        if self.in_sector(o.x,o.y):
            self.o[x][y].append(o)
            if o.updates:
                self.uos.append(o)
        else:
            self.w.spawn(o)
    def spawnX(self,o):
        self.o[o.x][o.y].append(o)
        o.x+=self.x*16
        o.y+=self.y*16
        if o.updates:
            self.uos.append(o)
    def in_sector(self,x,y):
        x,y=self.d_pos(x,y)
        return 0<=x<self.size[0] and 0<=y<self.size[1]
    def is_clear(self,x,y):
        if not self.in_sector(x,y):
            return self.w.is_clear(x,y)
        for o in self.get_os(x,y):
            if o.solid:
                return False
        return Tiles.tiles[self.get_t(x,y)].passable
    def get_t(self,x,y):
        if not self.in_sector(x,y):
            return self.w.get_t(x,y)
        x,y=self.d_pos(x,y)
        return self.t[x][y]
    def dest(self,o):
        x,y=self.d_pos(o.x,o.y)
        self.o[x][y].remove(o)
        if o in self.uos:
            self.uos.remove(o)
    def move(self,o,tx,ty):
        self.dest(o)
        o.x=tx
        o.y=ty
        if not self.in_sector(tx,ty):
            self.w.spawn(o)
            if o in self.uos:
                self.uos.remove(o)
        else:
            self.spawn(o)
    def get_os(self,x,y):
        if not self.in_sector(x,y):
            return self.w.get_os(x,y)
        x,y=self.d_pos(x,y)
        return self.o[x][y]
    def get_o(self,x,y):
        x,y=self.d_pos(x,y)
        os=self.get_os(x,y)
        if os:
            return os[0]
    def d_pos(self,x,y):
        return x-self.x*16,y-self.y*16
class HomeSector(Sector):
    def __init__(self,w,x,y,ps):
        Sector.__init__(self,w,x,y)
        for p in ps:
            self.spawn(p)
    def build(self):
        self.spawnX(Objects.SellPoint(7,7,self))