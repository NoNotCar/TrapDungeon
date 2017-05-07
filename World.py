import Tiles
import Objects
import pygame
from random import randint, choice
import Img
import Players
import Direction as D
import Biomes
from NoiseGen import perlin
from math import ceil
bnoise=None
bnoise2=None
tnoise=None
def makenoise():
    global bnoise,bnoise2
    bnoise=perlin.SimplexNoise(256)
    bnoise2=perlin.SimplexNoise(256)
    global tnoise
    tnoise=perlin.SimplexNoise(256)
cashfont=Img.fload("cool",32)
bscale=128.0
b2scale=160.0
bcfont=Img.fload("cool",64)
threshold=1.2
exp=Img.sndget("bomb")
def ir(n):
    return int(round(n))
numerals=Img.imgstripxf("Numbers",5)+[Img.imgx("Ten")]
scales=[16,32,48,64]
class World(object):
    is_done=False
    winner=None
    invscale=3
    wscale=2
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
                p.die(self.get_sector(p))
            elif p.dead:
                if p.dt:
                    p.dt-=1
                else:
                    p.dead.update()
                    if p.dead.t<=0:
                        if not p.home.respawn(p):
                            p.dead.t=60
                        else:
                            p.dead=None
        if drects:
            for e in enemies:
                if not e.denemy and e.rect.collidelist(drects)!=-1:
                    self.get_sector(e).dest(e)
                    e.die(self)
        self.eup(events)
    def eup(self,events):
        pass
    def render(self,p,screen):
        screenrect=screen.get_rect()
        sh,sw=screenrect.h,screenrect.w
        awscale=scales[self.wscale]
        aiscale=scales[self.invscale]
        riscale=self.invscale+1
        m=(sw/float(awscale)+1)/2.0
        rm=int(ceil(m))
        wconvmult=awscale/64.0
        if not (p.shop or (p.dead and not p.dt)):
            asx=p.x*awscale+ir(p.xoff)*wconvmult-(m-1)*awscale
            asy=p.y*awscale+ir(p.yoff)*wconvmult-(m-1)*awscale-aiscale
            r=(p.rumbling-1)//10+1
            rx=randint(-r,r)
            ry=randint(-r,r)
            sx=p.x
            sy=p.y
            for y in range(sy-rm-1,sy+rm+1):
                for x in range(sx-rm-1,sx+rm+1):
                    screen.blit(Tiles.tiles[self.get_t(x,y)].get_img()[self.wscale],(x*awscale-asx+rx,y*awscale-asy+ry))
            for y in range(sy-rm-1,sy+rm+1):
                for x in range(sx-rm-1,sx+rm+1):
                    objs=self.get_os(x,y)
                    for o in objs:
                        if not o.is_hidden(self,p):
                            screen.blit(o.get_img(self)[self.wscale],(x*awscale+ir(o.xoff)*wconvmult-asx+rx,y*awscale+ir(o.yoff)*wconvmult-asy-o.o3d*(self.wscale+1)+ry))
            pygame.draw.rect(screen,(200,200,200),pygame.Rect(0,0,sw,aiscale))
            for n,i in enumerate(p.iinv.inv if p.iinv else p.inv):
                screen.blit(i.get_img(p,self)[self.invscale],(n*aiscale,0))
                if i.stack>1:
                    screen.blit(numerals[i.stack-2][self.invscale],(n*aiscale+(11 if i.stack<10 else 9)*(self.invscale+1),36))
                if n==p.isel:
                    pygame.draw.rect(screen,p.col,pygame.Rect(n*aiscale,15*riscale,aiscale,riscale))
            if p.statuseffects:
                maxt=max([se[1] for se in p.statuseffects])
                maxse=[se for se in p.statuseffects if se[1]==maxt][0]
                pygame.draw.rect(screen,p.col,pygame.Rect(0,sh-9,maxt*sw//Players.etimes[maxse[0]],12))
        elif p.shop:
            screen.fill((150,150,150))
            pygame.draw.rect(screen,(200,200,200),pygame.Rect(0,0,sw,64))
            Img.bcentrex(bcfont,p.shop.title,screen,-16)
            for n,i in enumerate(p.shop.items):
                Img.cxblit(i[0].img[self.invscale],screen,n*aiscale+aiscale,-8*riscale)
                Img.bcentrex(cashfont,str(i[1]),screen,n*aiscale+aiscale,(255,255,0),8*riscale)
            screen.blit(p.simg[self.invscale],(0,p.ssel*aiscale+aiscale))
        else:
            p.dead.render(screen)
        Img.bcentrex(cashfont,str(p.cash),screen,sh-48,(255,255,0))
        pygame.draw.rect(screen,p.col,pygame.Rect(0,0,sw,sh),2)
    def get_t(self,x,y):
        sx=x//16
        sy=y//16
        try:
            return self.w[(sx,sy)].get_t(x,y)
        except KeyError:
            self.new_sector(sx,sy)
            return self.get_t(x,y)
    def get_tclass(self,x,y):
        return self.get_psector(x,y).get_tclass(x,y)
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
    def change_t(self,x,y,t):
        self.get_psector(x,y).change_t(x,y,t)
    def get_sector(self,o):
        sx=o.x//16
        sy=o.y//16
        try:
            return self.w[(sx,sy)]
        except KeyError:
            self.new_sector(sx,sy)
            return self.get_sector(o)
    def get_psector(self,x,y):
        sx=x//16
        sy=y//16
        try:
            return self.w[(sx,sy)]
        except KeyError:
            self.new_sector(sx,sy)
            return self.get_psector(x,y)
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
        for x,y in self.iterlocs():
            biome=Biomes.convert(bnoise.noise2(x/bscale,y/bscale),bnoise2.noise2(x/b2scale,y/b2scale))
            self.change_t(x,y,biome.floor)
            noise=tnoise.noise2(x/16.0, y/16.0)+1
            if not randint(0,600):
                if randint(0,2):
                    self.spawn(Objects.UpgradePoint(x,y))
                else:
                    self.spawn(Objects.DodgyShop(x, y))
            elif noise<threshold:
                biome.GenerateWall(x,y,self)
            else:
                biome.GenerateSpace(x,y,self,noise)
    def oconvert(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.o[x][y]=[]
        self.uos=[]
    def update(self,events):
        for o in self.uos[:]:
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
    def reg_updates(self,o):
        self.uos.append(o)
    def spawnX(self,o):
        self.o[o.x][o.y].append(o)
        o.place(o.x+self.x*16,o.y+self.y*16)
        if o.updates:
            self.uos.append(o)
    def in_sector(self,x,y):
        x,y=self.d_pos(x,y)
        return 0<=x<self.size[0] and 0<=y<self.size[1]
    def is_clear(self,x,y,e,ignore_passable=False):
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
        return self.get_tclass(x,y).passable or e in self.w.ps or ignore_passable
    def get_t(self,x,y):
        if not self.in_sector(x,y):
            return self.w.get_t(x,y)
        x,y=self.d_pos(x,y)
        return self.t[x][y]
    def get_tclass(self,x,y):
        return Tiles.tiles[self.get_t(x,y)]
    def change_t(self,x,y,t):
        if not self.in_sector(x,y):
            return self.w.change_t(x,y,t)
        x,y=self.d_pos(x,y)
        self.t[x][y]=t
    def dest(self,o):
        x,y=self.d_pos(o.x,o.y)
        if self.in_sector(o.x,o.y):
            try:
                self.o[x][y].remove(o)
            except ValueError:
                print "WARNING: object %s not in sector" % o
            if o in self.uos:
                self.uos.remove(o)
        else:
            self.w.dest(o)
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
    def iter_players(self,x,y):
        for p in self.w.ps:
            dist=abs(p.x-x)+abs(p.y-y)
            yield p,dist
    def create_exp(self, fx, fy, r, exps):
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
        elif exps=="Circle":
            for x in range(fx-r,fx+r+1):
                for y in range(fy-r,fy+r+1):
                    if (x-fx)**2+(y-fy)**2<(r+0.5)**2:
                        self.explode(x,y)
        for p,d in self.iter_players(fx,fy):
            if d<r*3:
                p.rumbling=(r*3-d)*10
        exp.play()
    def explode(self, x, y):
        gos=self.get_os(x,y)
        rt=False
        for o in gos:
            if o.solid:
                if o.explodes:
                    rt=True
                    self.w.dest(o)
                    o.explode(self)
                    self.w.spawn(Objects.Explosion(x, y))
                elif o.enemy or o in self.w.ps:
                    pass
                else:
                    rt=True
                    o.explode(self)
            else:
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
    def __init__(self,w,x,y,ps,sellpoint=Objects.SellPoint,spargs=()):
        self.sp=sellpoint
        self.spa=spargs
        Sector.__init__(self,w,x,y)
        for p in ps:
            self.spawnX(p)
            p.home=self
    def build(self):
        self.spawnX(self.sp(7,7,self,*self.spa))
        for x,y in self.iterlocs():
            if (x in [0,15] or y in [0,15]) and randint(0,1):
                biome=Biomes.convert(bnoise.noise2(x/bscale,y/bscale),bnoise2.noise2(x/b2scale,y/b2scale))
                self.change_t(x,y,biome.floor)
                noise=tnoise.noise2(x/16.0, y/16.0)+1
                if noise<threshold:
                    biome.GenerateWall(x,y,self)
                else:
                    biome.GenerateSpace(x,y,self,noise)
            else:
                self.change_t(x,y,7)
    def respawn(self,p):
        attempts=0
        while attempts<100:
            x=randint(0,15)
            y=randint(0,15)
            if not self.get_os(x,y):
                p.place(x,y)
                self.spawnX(p)
                return True
            attempts+=1
        return False
class Glade(Sector):
    def build(self):
        self.r=randint(4,8)
        for x,y in self.iterlocs():
            ax,ay=self.d_pos(x,y)
            biome=Biomes.convert(bnoise.noise2(x/bscale,y/bscale),bnoise2.noise2(x/b2scale,y/b2scale))
            dx=abs(ax-7.5)
            dy=abs(ay-7.5)
            if (dx**2+dy**2)**0.5<self.r:
                self.change_t(x,y,1)
                if not(ax in [7,8] and ay in [7,8]) and randint(0,1):
                    self.spawn(Objects.Tree(x,y))
            else:
                self.change_t(x,y,biome.floor)
                noise=tnoise.noise2(x/16.0, y/16.0)+1
                if not randint(0,600):
                    self.spawn(Objects.UpgradePoint(x,y))
                elif noise<threshold:
                    biome.GenerateWall(x,y,self)
                else:
                    biome.GenerateSpace(x,y,self,noise)
        self.spawnX(Objects.GSellPoint(7,7,self))