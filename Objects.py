from BaseClasses import Object, MultiPart
from Img import breakimgs, imgx, sndget, imgstripx,imgstripxf, imgrot, colswap, colcopy, teamcolours
import Items
from Shop import Shop, GPUpgrade, SpeedUpgrade
from random import randint
from pygame import Rect
import Direction as D
breaksnd=sndget("break")
pickup=sndget("pickup")
missile=sndget("missile")
csh=sndget("cash")
class Wall(Object):
    o3d = 4
    imgs=breakimgs("Rock")
    blevel=0
    name="Wall"
    explodes = True
    hardness=8
    def get_img(self,world):
        return self.imgs[((self.blevel-self.hardness+1)//self.hardness)+1]
    def pick(self,world,strength=1):
        self.blevel+=strength
        if self.blevel>=self.hardness*9-1:
            world.dest(self)
            breaksnd.play()
        return True
class Tree(Object):
    o3d=7
    img=imgx("Tree")
    explodes = True
class IceWall(Wall):
    imgs = breakimgs("IceBlock")
class Obsidian(Wall):
    imgs=breakimgs("Obsidian")
    hardness = 16
class GreyWall(Wall):
    imgs=breakimgs("GreyWall")
class SandWall(Wall):
    imgs=breakimgs("DesertWall")
class DarkObsidian(Object):
    img=imgx("DarkObsidian")
    o3d = 4
    explodes = True
class InsaniumOre(Object):
    img=imgx("InsaniumOre")
    o3d = 4
    explodes = True
    def explode(self,world):
        world.spawn(Insanium(self.x,self.y))
class HuntedBox(Object):
    img=imgx("HuntedBox")
    o3d = 4
    explodes = True
    boxcolours=((255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255),(255,128,0))
    def __init__(self,x,y,n):
        self.place(x,y)
        self.img=self.img.copy()
        colswap(self.img,(128,128,128),self.boxcolours[n])
    def explode(self,world):
        world.w.boxlocs.remove((self.x,self.y))
class GoldOre(Wall):
    imgs=breakimgs("GoldRock")
    hardness = 12
    def pick(self,world,strength=1):
        self.blevel+=strength
        if self.blevel>=self.hardness*9-1:
            world.dest(self)
            world.spawn(Gold(self.x,self.y))
            breaksnd.play()
        return True
    def explode(self,world):
        world.spawn(Gold(self.x,self.y))
class ExpBox(Object):
    imgs=imgstripxf("ExpBlock",16)
    countdown=60
    o3d=4
    def explode(self,world):
        if not self.updates:
            self.updates=True
            world.reg_updates(self)
    def pick(self,world,strength=1):
        self.explode(world)
    def update(self,world,events):
        self.countdown-=1
        if not self.countdown:
            world.dest(self)
            world.create_exp(self.x, self.y, 2, "Cross")
    def get_img(self,world):
        return self.imgs[0 if self.countdown==60 else self.countdown%8//4+1]
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
    img = imgx("Bomb")
    name = "Bomb"
    def __init__(self, x, y, p ,r=2):
        self.x = x
        self.y = y
        self.r = r
class Dynamite(Explosive):
    imgs=imgstripx("Dynamite")
    img=imgs[0]
    name="Dynamite"
    expshape = "Square"
    r=1
    timer=239
    def get_img(self,world):
        return self.imgs[7-(self.timer//30)]
class Trap(Object):
    solid=False
    hidden=True
    deactivates=False
    def __init__(self,x,y,p):
        self.owner=p
        self.place(x,y)
    def walkover(self,p,world):
        if not self.deactivates or self.hidden:
            self.trap(p,world)
    def trap(self,p,world):
        pass
    def is_hidden(self,world,p):
        return p is not self.owner and self.hidden
    def pick(self,world,strength=1):
        if not self.hidden:
            world.dest(self)
            breaksnd.play()
    def explode(self,world):
        world.dest(self)
    def emp(self,world):
        self.hidden=False
class Mine(Trap):
    name="Mine"
    img=imgx("Mine")
    dimg=imgx("MineDeact")
    deactivates = True
    def trap(self,p,world):
        self.explode(world)
    def explode(self,world):
        world.dest(self)
        world.create_exp(self.x,self.y,1,"Square")
    def get_img(self,world):
        return self.img if self.hidden else self.dimg
class BarbedWire(Trap):
    name="BarbedWire"
    img=imgx("BarbedWire")
    snd=sndget("barbs")
    def trap(self,p,world):
        if p.name=="Player":
            p.add_effect("Pause")
            self.snd.play()
        world.dest(self)
class Missile(Object):
    enemy = True
    denemy = True
    img=imgx("Missile")
    fimgs=imgrot(imgx("MissileIF"))
    orect = Rect(24,12,16,44)
    speed = 1
    aspeed=1
    name="Missile"
    updates = True
    flying = True
    exp=(1,"Square")
    def __init__(self,x,y,firer):
        self.place(x,y)
        self.d=firer.d
        self.dire=D.get_dir(firer.d)
        missile.play()
    def update(self,world,events):
        if self.aspeed<16:
            self.aspeed+=1
            self.speed=self.aspeed//2
        if not self.moving:
            if not self.move(self.dire[0],self.dire[1],world):
                world.dest(self)
                world.create_exp(self.x,self.y,*self.exp)
    def get_img(self,world):
        return self.fimgs[self.d]
class NuclearMissile(Missile):
    name="NMissile"
    img = imgx("NMissile")
    fimgs = imgrot(imgx("NMissileIF"))
    exp=(5,"Circle")
class Explosion(Object):
    img = imgx("Exp")
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
    img=imgx("CashPoint")
    name = "Shop"
    shop=Shop([(Mine,40),(Items.Compass,50),(Bomb,20),(Missile,50)])
    def __init__(self,x,y,world):
        self.place(x,y)
        for dx,dy in ((0,1),(1,0),(1,1)):
            tx=x+dx
            ty=y+dy
            world.spawnX(MultiPart(tx,ty,self))
    def interact(self,world,p):
        sold=False
        for i in p.get_all_items()[:]:
            if i.value:
                sold=True
                p.cash+=i.value*i.stack if i.stack else i.value
                p.remove_item(i)
        if sold:
            csh.play()
        else:
            p.shop=self.shop
            p.ssel=0
class FlagPoint(SellPoint):
    img=imgx("FlagPoint")
    name = "Shop"
    alarm=sndget("alarm")
    def __init__(self,x,y,world,team):
        self.t=team
        self.img=colcopy(self.img,(0,0,255),tuple(c*4//5 for c in teamcolours[team]))
        colswap(self.img,(0,0,127),tuple(c//2 for c in teamcolours[team]))
        SellPoint.__init__(self,x,y,world)
        self.flag=Items.Flag(teamcolours[team],self)
        self.re_img()
        self.shop = Shop([(Mine, 40), ((Items.RedCompass if team else Items.BlueCompass), 50), (Bomb, 20), (Missile, 50),(BarbedWire,5)])
    def interact(self,world,p):
        flags=[i for i in p.get_all_items() if i.name=="Flag"]
        if flags:
            if self.flag:
                world.w.is_done=True
                world.w.winner=self.t
        elif p.team!=self.t:
            if self.flag:
                if p.add_item(self.flag):
                    self.flag=None
                    self.re_img()
                    self.alarm.play()
        else:
            sold=False
            for i in p.get_all_items()[:]:
                if i.value:
                    sold=True
                    p.cash+=i.value*i.stack if i.stack else i.value
                    p.remove_item(i)
            if sold:
                csh.play()
            else:
                p.shop=self.shop
                p.ssel=0
    def re_img(self):
        self.aimg=self.img.copy()
        if self.flag:
            self.aimg.blit(self.flag.img,(8,8))
    def get_img(self,world):
        return self.aimg
class GSellPoint(SellPoint):
    img = imgx("BCashPoint")
    shop = Shop([(Bomb,10),(Dynamite,20),(Items.GigaDrill,250)])
class UpgradePoint(Object):
    img=imgx("UpgradeStation")
    o3d = 4
    shop=Shop([(GPUpgrade,100),(SpeedUpgrade,50),(Items.BridgeBuilder,50),(Items.BagOfLoot,200),(Items.Defuser,100)],"UTILITIES")
    def interact(self,world,p):
        p.shop=self.shop
        p.ssel=0
class DodgyShop(Object):
    img=imgx("DodgyShop")
    o3d = 4
    shop=Shop([(Items.Pill,100),(NuclearMissile,250)],"DODGY SHOP")
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
    img=imgx("Diamond")
    value=50
class RedDiamond(ValuableObject):
    img = imgx("RedDiamond")
    value = 150
class Ruby(ValuableObject):
    img=imgx("Ruby")
    value = 30
    stacks = True
    name="Ruby"
class MiniDiamond(ValuableObject):
    img=imgx("MiniDiamond")
    value = 30
    stacks = True
    name="MiniDiamond"
class Gold(ValuableObject):
    img=imgx("GoldNugget")
    value = 50
    stacks = True
    name="Gold"
class Insanium(ValuableObject):
    img=imgx("Insanium")
    value = 300
    stacks = True
    name="Insanium"
class Tronics(ValuableObject):
    img=imgx("CPUCard")
    value = 100
    stacks = True
    name="Tronics"
