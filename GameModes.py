from World import World, Sector, bscale, threshold, Glade
import World as W
from random import randint, choice
import Biomes
from Objects import HuntedBox
import Objects
import Items
class BoxHuntWorld(World):
    def __init__(self,ps):
        World.__init__(self,ps)
        self.boxlocs=[]
        while len(self.boxlocs)<7:
            rx=choice([randint(-60,-40),randint(60,80)])
            ry=choice([randint(-60,-40),randint(60,80)])
            if (rx,ry) not in self.boxlocs:
                self.boxlocs.append((rx,ry))
    def new_sector(self,sx,sy):
        d=abs(sx)+abs(sy)
        bhuntlocs=[]
        bhuntns=[]
        for n,bl in enumerate(self.boxlocs):
            bx,by=bl
            if sx*16<=bx<sx*16+16 and sy*16<=by<sy*16+16:
                bhuntlocs.append((bx,by))
                bhuntns.append(n)
        if bhuntlocs:
            self.w[(sx,sy)]=BoxHuntSector(self,sx,sy,bhuntlocs,bhuntns)
        elif d<5 or randint(0,10):
            self.w[(sx,sy)]=Sector(self,sx,sy)
        else:
            self.w[(sx,sy)]=Glade(self,sx,sy)
    def is_done(self):
        return not len(self.boxlocs)
    def get_nearest_box(self,x,y):
        nearbs=[]
        maxdist=None
        for bx,by in self.boxlocs:
            dist=abs(bx-x)+abs(by-y)
            if maxdist is None or dist<maxdist:
                maxdist=dist
                nearbs=[(bx,by)]
            elif dist==maxdist:
                nearbs.append((bx,by))
        return nearbs[0]
class BoxHuntSector(Sector):
    def __init__(self,w,x,y,boxes,boxnums):
        self.boxes=boxes
        self.boxnums=boxnums
        Sector.__init__(self,w,x,y)
    def build(self):
        for x,y in self.iterlocs():
            biome=Biomes.convert(W.bnoise.noise2(x/bscale,y/bscale))
            self.change_t(x,y,biome.floor)
            noise=W.tnoise.noise2(x/16.0, y/16.0)+1
            if (x,y) in self.boxes:
                self.spawn(HuntedBox(x,y,self.boxnums[self.boxes.index((x,y))]))
            elif noise<threshold:
                biome.GenerateWall(x,y,self)
            else:
                biome.GenerateSpace(x,y,self,noise)
class GameMode(object):
    name="Gamemode"
    maxp=8
    timereverse=False
    world=World
    largescreen=False
    def create_inv(self):
        return None
class Standard(GameMode):
    name="Standard"
    def create_inv(self):
        return [Items.Pickaxe(),Items.StackPlacer(Objects.Bomb,3),Items.StackPlacer(Objects.Mine)]
class Duo(Standard):
    name="Duo"
    largescreen = True
    maxp = 2
class BoxHunt(GameMode):
    name="Box Hunt"
    maxp = 1
    world=BoxHuntWorld
    timereverse = True
    largescreen = True
    def create_inv(self):
        return [Items.Pickaxe(),Items.StackPlacer(Objects.Bomb,3),Items.StackPlacer(Objects.Mine),Items.BHCompass()]
gamemodes=[Standard(),Duo(),BoxHunt()]