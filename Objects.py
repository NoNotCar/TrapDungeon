from BaseClasses import Object, MultiPart
from Img import breakimgs, img4, sndget
import Items
from Shop import Shop
import Traps
from random import randint
from pygame import Rect
breaksnd=sndget("break")
pickup=sndget("pickup")
class Wall(Object):
    o3d = 4
    imgs=breakimgs("Rock")
    blevel=0
    explodes = True
    def get_img(self,world):
        return self.imgs[((self.blevel-7)//8)+1]
    def pick(self,world):
        self.blevel+=1
        if self.blevel==71:
            world.dest(self)
            breaksnd.play()
class SellPoint(Object):
    o3d = 4
    img=img4("CashPoint")
    name = "Shop"
    def __init__(self,x,y,world):
        self.place(x,y)
        for dx,dy in ((0,1),(1,0),(1,1)):
            tx=x+dx
            ty=y+dy
            world.spawn(MultiPart(tx,ty,self))
    def interact(self,world,p):
        p.shop=Shop([(Traps.SlowTrap,20),(Traps.FastTrap,20),(Traps.ReverseTrap,50),(Traps.PauseTrap,100),(Items.Compass,50),(Bomb,20)])
        p.ssel=0
class Diamond(Object):
    img=img4("Diamond")
    def interact(self,world,p):
        if p.add_item(Items.Diamond()):
            world.dest(self)
            pickup.play()
class Bomb(Object):
    timer = 120
    img = img4("Bomb")
    name = "Bomb"
    updates = True
    def __init__(self, x, y, r=2):
        self.x = x
        self.y = y
        self.r = r

    def update(self, world, events):
        self.timer -= 1
        if self.timer == 0:
            world.dest(self)
            world.create_exp(self.x, self.y, self.r)
        elif self.timer <= 30:
            self.xoff = randint(-2, 2)
            self.yoff = randint(-2, 2)
    def explode(self,world):
        self.timer=1
class Explosion(Object):
    img = img4("Exp")
    orect = Rect(12, 12, 40, 40)
    life = 20
    enemy = True
    denemy = True
    updates=True

    def update(self, world, events):
        self.xoff = randint(-1, 1)
        self.yoff = randint(-1, 1)
        self.life -= 1
        if self.life == 0:
            world.dest(self)
