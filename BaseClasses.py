from Img import blank64
import pygame
class Object(object):
    img=None
    speed=4
    xoff,yoff=(0,0)
    orect=pygame.Rect(0,0,64,64)
    moving=False
    o3d=0
    solid=True
    name="Object"
    updates=False
    enemy=False
    denemy=False
    exclude=[]
    explodes=False
    flying=False
    dx=0
    dy=0
    def __init__(self,x,y):
        self.place(x,y)
        self.rerect()
    def place(self,x,y):
        self.x=x
        self.y=y
        self.rerect()
    def update(self,world,events):
        pass
    def get_img(self,world):
        return self.img
    def mupdate(self,world):
        if self.xoff>0:
            self.xoff-=self.speed
        elif self.xoff<0:
            self.xoff+=self.speed
        if self.yoff>0:
            self.yoff-=self.speed
        elif self.yoff<0:
            self.yoff+=self.speed
        if abs(self.xoff)<self.speed and abs(self.yoff)<self.speed:
            self.xoff=0
            self.yoff=0
            self.moving=False
            if self.name=="Player":
                for o in world.get_os(self.x,self.y):
                    o.walkover(self,world)
                if not world.get_tclass(self.x,self.y).passable:
                    self.sinking=1
            if not self.flying and world.get_tclass(self.x,self.y).slippery:
                self.move(self.dx,self.dy,world)
        self.rerect()
    def move(self,dx,dy,world,ignoreobs=False):
        tx=self.x+dx
        ty=self.y+dy
        if world.is_clear(tx,ty,self,self.flying) or ignoreobs:
            world.move(self,tx,ty)
            self.moving=True
            self.xoff= -dx*64
            self.yoff= -dy*64
            self.dx=dx
            self.dy=dy
            return True
        return False
    def interact(self,world,p):
        pass
    def pick(self,world,strength=1):
        pass
    def walkover(self,p,world):
        pass
    def rerect(self):
        self.rect=self.orect.move(self.x*64+self.xoff,self.y*64+self.yoff)
    def explode(self,world):
        pass
    def is_hidden(self,world,p):
        return False
class MultiPart(Object):
    img=blank64
    def __init__(self,x,y,p):
        self.p=p
        self.solid=p.solid
        self.place(x,y)
        self.name=p.name
    def interact(self,world,p):
        self.p.interact(world,p)