from BaseClasses import Object, MultiPart
from Img import breakimgs, img4, sndget, imgstrip4
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
class Tree(Object):
    o3d=7
    img=img4("Tree")
    explodes = True
class Explosive(Object):
    timer = 120
    updates = True
    r=2
    expshape="Cross"
    def update(self, world, events):
        self.timer -= 1
        if self.timer == 0:
            world.dest(self)
            world.create_exp(self.x, self.y, self.r, self.expshape)
        elif self.timer <= 30:
            self.xoff = randint(-2, 2)
            self.yoff = randint(-2, 2)
    def explode(self,world):
        self.timer=1
class Bomb(Explosive):
    img = img4("Bomb")
    name = "Bomb"
    def __init__(self, x, y, r=2):
        self.x = x
        self.y = y
        self.r = r
class Dynamite(Explosive):
    imgs=imgstrip4("Dynamite")
    img=imgs[0]
    name="Dynamite"
    expshape = "Square"
    r=1
    timer=239
    def get_img(self,world):
        return self.imgs[7-(self.timer//30)]
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
class SellPoint(Object):
    o3d = 4
    img=img4("CashPoint")
    name = "Shop"
    shop=Shop([(Traps.SlowTrap,20),(Traps.ReverseTrap,50),(Traps.PauseTrap,100),(Items.Compass,50),(Bomb,20),(Items.FFToken,20)])
    def __init__(self,x,y,world):
        self.place(x,y)
        for dx,dy in ((0,1),(1,0),(1,1)):
            tx=x+dx
            ty=y+dy
            world.spawn(MultiPart(tx,ty,self))
    def interact(self,world,p):
        p.shop=self.shop
        p.ssel=0
class GSellPoint(SellPoint):
    img = img4("BCashPoint")
    shop = Shop([(Bomb,10),(Dynamite,20)])
class ValuableObject(Object):
    value=100
    stacks=False
    def interact(self,world,p):
        if p.add_item(Items.StackValuables(self) if self.stacks else Items.ValuableItem(self)):
            world.dest(self)
            pickup.play()
class Diamond(ValuableObject):
    img=img4("Diamond")
    value=50
class RedDiamond(ValuableObject):
    img = img4("RedDiamond")
    value = 250
class Ruby(ValuableObject):
    img=img4("Ruby")
    value = 30
    stacks = True
    name="Ruby"

