from BaseClasses import Object, MultiPart
from Img import breakimgs, img4, sndget, imgstrip4, imgrot
import Items
from Shop import Shop, GPUpgrade, SpeedUpgrade
import Traps
from random import randint
from pygame import Rect
import Direction as D
breaksnd=sndget("break")
pickup=sndget("pickup")
missile=sndget("missile")
class Wall(Object):
    o3d = 4
    imgs=breakimgs("Rock")
    blevel=0
    name="Wall"
    explodes = True
    def get_img(self,world):
        return self.imgs[((self.blevel-7)//8)+1]
    def pick(self,world,strength=1):
        self.blevel+=strength
        if self.blevel>=71:
            world.dest(self)
            breaksnd.play()
        return True
class Tree(Object):
    o3d=7
    img=img4("Tree")
    explodes = True
class IceWall(Wall):
    imgs = breakimgs("IceBlock")
class Explosive(Object):
    timer = 120
    updates = True
    r=2
    expshape="Cross"
    def __init__(self,x,y,p):
        self.place(x,y)
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
    def __init__(self, x, y, p ,r=2):
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
class Missile(Object):
    enemy = True
    denemy = True
    img=img4("Missile")
    fimgs=imgrot(img4("MissileIF"))
    orect = Rect(24,12,16,44)
    speed = 8
    name="Missile"
    updates = True
    def __init__(self,x,y,firer):
        self.place(x,y)
        self.d=firer.d
        self.dire=D.get_dir(firer.d)
        missile.play()
    def update(self,world,events):
        if not self.moving:
            if not self.move(self.dire[0],self.dire[1],world):
                world.dest(self)
                world.create_exp(self.x,self.y,1,"Square")
    def get_img(self,world):
        return self.fimgs[self.d]
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
    shop=Shop([(Traps.SlowTrap,20),(Traps.ReverseTrap,40),(Traps.PauseTrap,80),(Items.Compass,50),(Bomb,20),(Items.FFToken,20)])
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
    shop = Shop([(Bomb,10),(Dynamite,20),(Items.GigaDrill,250)])
class UpgradePoint(Object):
    img=img4("UpgradeStation")
    o3d = 4
    shop=Shop([(GPUpgrade,100),(SpeedUpgrade,50),(Missile,30)])
    def interact(self,world,p):
        p.shop=self.shop
        p.ssel=0
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
class Tronics(ValuableObject):
    img=img4("CPUCard")
    value = 100
    stacks = True
    name="Tronics"
