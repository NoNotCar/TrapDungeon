import Tiles
import Objects
import pygame
from random import randint, choice
import Img
import Players
import Direction as D
import Biomes
from NoiseGen import perlin
def makenoise():
    global bnoise
    bnoise=perlin.SimplexNoise(256)
    global tnoise
    tnoise=perlin.SimplexNoise(256)
cashfont=Img.fload("cool",32)
bscale=8.0
bcfont=Img.fload("cool",64)
threshold=1.3
exp=Img.sndget("bomb")
numerals=Img.imgstrip4f("Numbers",5)+[Img.img4("Ten")]
class World(object):
    m=5
    def __init__(self,ps):
        hs=HomeSector(self,0,0,ps)
        self.ps=ps
        self.w={(0,0):hs}
    def update(self,events):
        for s in [s for s in self.w.itervalues()]:
            s.update(events)
        erects=[]
        enemies=[]
        drects=[]
        for s in self.w.itervalues():
            for e in s.uos:
                if e.enemy:
                    erects.append(e.rect)
                    enemies.append(e)
                if e.denemy:
                    drects.append(e.rect)
        for p in self.ps:
            if not p.dead and p.rect.collidelist(erects)!=-1:
                p.die()
            elif p.dead:
                p.dead-=10 if all([op.dead for op in self.ps]) else 1
                if p.dead<=0:
                    if not self.w[(0,0)].respawn(p):
                        p.dead=60
        if drects:
            for e in enemies:
                if not e.denemy and e.rect.collidelist(drects)!=-1:
                    self.get_sector(e).dest(e)
                    e.die(self)
    def render(self,p,screen):
        if not (p.shop or p.dead):
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
                        if not o.is_hidden(self,p):
                            screen.blit(o.get_img(self),(x*64+o.xoff-asx,y*64+o.yoff-asy-o.o3d*4))
            pygame.draw.rect(screen,(200,200,200),pygame.Rect(0,0,448,64))
            for n,i in enumerate(p.inv):
                screen.blit(i.get_img(p),(n*64,0))
                if i.stack>1:
                    screen.blit(numerals[i.stack-2],(n*64+(44 if i.stack<10 else 36),36))
                if n==p.isel:
                    pygame.draw.rect(screen,p.col,pygame.Rect(n*64,60,64,4))
            if p.statuseffects:
                maxt=max([se[1] for se in p.statuseffects])
                maxse=[se for se in p.statuseffects if se[1]==maxt][0]
                pygame.draw.rect(screen,p.col,pygame.Rect(0,507,maxt*448//Players.etimes[maxse[0]],12))
        elif p.shop:
            screen.fill((150,150,150))
            pygame.draw.rect(screen,(200,200,200),pygame.Rect(0,0,448,64))
            Img.bcentrex(bcfont,"SHOP",screen,-16)
            for n,i in enumerate(p.shop.items):
                Img.cxblit(i[0].img,screen,n*64+64,-32)
                Img.bcentrex(cashfont,str(i[1]),screen,n*64+64,(255,255,0),32)
            screen.blit(p.simg,(0,p.ssel*64+64))
        else:
            Img.bcentre(bcfont,"DEAD",screen,col=(255,255,255))
            Img.bcentre(cashfont,"RESPAWN: "+str(p.dead//60),screen,64,(255,255,255))
        Img.bcentrex(cashfont,str(p.cash),screen,468,(255,255,0))
        pygame.draw.rect(screen,p.col,pygame.Rect(0,0,448,516),2)
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
        d=abs(sx)+abs(sy)
        if d<5 or randint(0,10):
            self.w[(sx,sy)]=Sector(self,sx,sy)
        else:
            self.w[(sx,sy)]=Glade(self,sx,sy)
    def is_clear(self,x,y,e):
        sx=x//16
        sy=y//16
        try:
            return self.w[(sx,sy)].is_clear(x,y,e)
        except KeyError:
            self.new_sector(sx,sy)
            return self.is_clear(x,y,e)
    def spawn(self,o):
        self.get_sector(o).spawn(o)
    def dest(self,o):
        self.get_sector(o).dest(o)
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
        self.d=abs(x)+abs(y)
        self.w=w
        self.build()
    def build(self):
        self.biome=Biomes.convert(bnoise.noise2(self.x/bscale,self.y/bscale))
        ebiomes={}
        nullbiomes=[]
        for dx,dy in D.directions:
            try:
                sbiome=self.w.w[D.offsetd((dx,dy),self)].biome
                if sbiome!=self.biome:
                    ebiomes[(dx,dy)]=sbiome
                else:
                    nullbiomes.append((dx,dy))
            except KeyError:
                nullbiomes.append((dx,dy))
        for x,y in self.iterlocs():
            biome=self.biome
            if len(ebiomes) and randint(0,1):
                try:
                    ax,ay=self.d_pos(x,y)
                    if (-1,0) not in nullbiomes and ax==0:
                        biome=ebiomes[(-1,0)]
                    elif (1,0) not in nullbiomes and ax==15:
                        biome=ebiomes[(1,0)]
                    elif (0,-1) not in nullbiomes and ay==0:
                        biome=ebiomes[(0,-1)]
                    elif (0,1) not in nullbiomes and ay==15:
                        biome=ebiomes[(0,1)]
                except KeyError:
                    pass
            self.change_t(x,y,biome.floor)
            noise=tnoise.noise2(x/16.0, y/16.0)+1
            if not randint(0,600):
                self.spawn(Objects.UpgradePoint(x,y))
            elif not randint(0,100):
                self.spawn((Objects.Diamond if self.d<8 else Objects.RedDiamond)(x,y))
            elif noise<threshold:
                biome.GenerateWall(x,y,self)
            else:
                biome.GenerateSpace(x,y,self,noise)
        self.biome.GenerateEx(self)
    def oconvert(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.o[x][y]=[]
        self.uos=[]
    def update(self,events):
        for o in self.uos:
            o.update(self,events)
            if o.moving:
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
        o.place(o.x+self.x*16,o.y+self.y*16)
        if o.updates:
            self.uos.append(o)
    def in_sector(self,x,y):
        x,y=self.d_pos(x,y)
        return 0<=x<self.size[0] and 0<=y<self.size[1]
    def is_clear(self,x,y,e):
        if not self.in_sector(x,y):
            return self.w.is_clear(x,y,e)
        for o in self.get_os(x,y):
            if o.solid:
                if e.denemy and o.enemy:
                    pass
                elif e not in self.w.ps and o not in self.w.ps:
                    return False
                elif not (e.enemy or o.enemy):
                    return False
        return self.get_tclass(x,y).passable or e in self.w.ps
    def get_t(self,x,y):
        if not self.in_sector(x,y):
            return self.w.get_t(x,y)
        x,y=self.d_pos(x,y)
        return self.t[x][y]
    def get_tclass(self,x,y):
        return Tiles.tiles[self.get_t(x,y)]
    def change_t(self,x,y,t):
        if not self.in_sector(x,y):
            raise NotImplementedError
        x,y=self.d_pos(x,y)
        self.t[x][y]=t
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
    def get_nearest_player(self,x,y):
        nearps=[]
        maxdist=None
        for p in self.w.ps:
            dist=abs(p.x-x)+abs(p.y-y)
            if maxdist is None or dist<maxdist:
                maxdist=dist
                nearps=[p]
            elif dist==maxdist:
                nearps.append(p)
        return choice(nearps), maxdist
    def create_exp(self, fx, fy, r, exps):
        exp.play()
        if exps=="Cross":
            self.explode(fx, fy)
            for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
                x, y = fx + dx, fy + dy
                for n in range(r):
                    if self.explode(x, y):
                        break
                    x += dx
                    y += dy
        elif exps=="Square":
            for x in range(fx-r,fx+r+1):
                for y in range(fy-r,fy+r+1):
                    self.explode(x,y)
    def explode(self, x, y):
        gos=self.get_os(x,y)
        rt=False
        for o in gos:
            if o.solid:
                if o.explodes:
                    rt=True
                    self.w.dest(o)
                    self.w.spawn(Objects.Explosion(x, y))
                elif o.enemy or o in self.w.ps:
                    pass
                else:
                    rt=True
                    o.explode(self)
        if rt:
            return True
        else:
            self.w.spawn(Objects.Explosion(x, y))
    def iterlocs(self):
        for x in range(16):
            for y in range(16):
                yield x+self.x*16,y+self.y*16
class HomeSector(Sector):
    biome=Biomes.Cave()
    def __init__(self,w,x,y,ps):
        Sector.__init__(self,w,x,y)
        for p in ps:
            self.spawn(p)
    def build(self):
        self.spawn(Objects.SellPoint(7,7,self))
    def respawn(self,p):
        attempts=0
        while attempts<100:
            x=randint(0,15)
            y=randint(0,15)
            if not self.get_os(x,y):
                p.place(x,y)
                self.spawn(p)
                return True
            attempts+=1
        return False
class Glade(Sector):
    def build(self):
        self.biome=Biomes.Cave()
        self.r=randint(4,8)
        for x in range(16):
            for y in range(16):
                noise=tnoise.noise2((self.x+x/16.0)*2, (self.y+y/16.0)*2)+1
                dx=abs(x-5.5)
                dy=abs(y-5.5)
                if (dx**2+dy**2)**0.5<self.r:
                    self.t[x][y]=1
                    if not(x in [7,8] and y in [7,8]) and randint(0,1):
                        self.spawnX(Objects.Tree(x,y))
                elif noise<threshold:
                    self.spawnX(Objects.Wall(x,y))
        self.spawn(Objects.GSellPoint(7+self.x*16,7+self.y*16,self))