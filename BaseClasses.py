from Img import blank64
class Object(object):
    img=None
    speed=4
    xoff,yoff=(0,0)
    moving=False
    o3d=0
    solid=True
    name="Object"
    updates=False
    def __init__(self,x,y):
        self.place(x,y)
    def place(self,x,y):
        self.x=x
        self.y=y
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
        if abs(self.xoff)<self.speed and abs(self.yoff)<self.speed and self.moving:
            self.xoff=0
            self.yoff=0
            self.moving=False
    def move(self,dx,dy,world):
        tx=self.x+dx
        ty=self.y+dy
        if world.is_clear(tx,ty):
            world.move(self,tx,ty)
            self.moving=True
            self.xoff= -dx*64
            self.yoff= -dy*64
            return True
        return False
    def interact(self,world,p):
        pass
    def pick(self,world):
        pass
class MultiPart(Object):
    img=blank64
    def __init__(self,x,y,p):
        self.p=p
        self.solid=p.solid
        self.place(x,y)
    def interact(self,world,p):
        self.p.interact(world,p)