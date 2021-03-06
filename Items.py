from Img import imgx, sndget, imgstripx, rot_center, colcopy
import Direction as D
import math
pickup=sndget("pickup")
defuse=sndget("EMP")
stackplacers=["Bomb","Dynamite","Missile","Mine","BarbedWire","NMissile"]
sixtyfourth=1.0/64
class Item(object):
    img=None
    continuous=False
    value=0
    stack=False
    name="Item"
    inv=None
    def get_img(self,p,world):
        return self.img
    def use(self,tars,world,tx,ty,p):
        pass
    def on_destroy(self):
        pass
class StackItem(Item):
    stack=1
    def use(self,tars,world,tx,ty,p):
        if self.stuse(tars,world,tx,ty,p):
            if self.stack==1:
                p.remove_item(self)
            else:
                self.stack-=1
    def stuse(self,tars,world,tx,ty,p):
        return True
class StackPlacer(StackItem):
    def __init__(self,oc,stack=1):
        self.img=oc.img
        self.name=oc.name
        self.c=oc
        self.stack=stack
    def stuse(self,tars,world,tx,ty,p):
        if not tars and (world.get_tclass(tx,ty).passable or self.c.flying):
            world.spawn(self.c(tx,ty,p))
            return True
class Pickaxe(Item):
    img=imgx("BasicPick")
    gimg=imgx("GoldenPick")
    name="Pickaxe"
    continuous = True
    golden=False
    def use(self,tars,world,tx,ty,p):
        if tars:
            tars[0].pick(world.w.get_sector(tars[0]),self.golden+1)
    def get_img(self,p,world):
        return self.gimg if self.golden else self.img
class Defuser(Item):
    imgs=imgstripx("Defuser")
    cooldown=0
    img=imgs[0]
    def get_img(self,p,world):
        if self.cooldown:
            self.cooldown-=1
        return self.imgs[bool(self.cooldown)]
    def use(self,tars,world,tx,ty,p):
        if not self.cooldown:
            defuse.play()
            for dx in range(-3,4):
                for dy in range(-3,4):
                    for o in world.get_os(p.x+dx,p.y+dy):
                        if o is not p:
                            o.emp(world)
            self.cooldown=600
class ValuableItem(Item):
    def __init__(self,oc):
        self.value=oc.value
        self.img=oc.img
        self.name=oc.name

class StackValuables(ValuableItem):
    stack = 1
def wrap(item):
    if item.name in stackplacers:
        return StackPlacer(item)
    return item()
class Trap(Item):
    def __init__(self,trapc):
        self.t=trapc
    def get_img(self,p,world):
        return self.t.img
    def use(self,tars,world,tx,ty,p):
        if not tars and world.get_tclass(tx,ty).passable:
            world.spawn(self.t(tx,ty,p))
            p.remove_item(self)
            pickup.play()
class Compass(Item):
    bimg=imgx("CompassBase")
    nimg=imgx("Needle")
    img=bimg.copy()
    img.blit(nimg,(0,0))
    imgs={}
    name="Compass"
    tpos=(7,7)
    def get_img(self,p,world):
        dx=p.x+p.xoff*sixtyfourth-self.tpos[0]
        dy=self.tpos[1]-p.y-p.yoff*sixtyfourth
        ang=int(round((math.degrees(math.atan2(dy,dx))+90)/30)*30)
        if ang not in self.imgs.keys():
            img=self.bimg.copy()
            img.blit(rot_center(self.nimg,ang),(0,0))
            self.imgs[ang]=img
        return self.imgs[ang]
class RedCompass(Compass):
    tpos=(-41,7)
class BlueCompass(Compass):
    tpos=(55,7)
class BHCompass(Item):
    bimg = imgx("CompassBase")
    nimg = imgx("BHNeedle")
    img = bimg.copy()
    img.blit(nimg, (0, 0))
    imgs={}
    name = "Compass"
    def get_img(self,p,world):
        bx,by=world.get_nearest_box(p.x,p.y)
        dx=p.x+p.xoff*sixtyfourth-bx
        dy=by-p.y-p.yoff*sixtyfourth
        ang = int(round((math.degrees(math.atan2(dy, dx)) + 90) / 30) * 30)
        if ang not in self.imgs.keys():
            img = self.bimg.copy()
            img.blit(rot_center(self.nimg, ang), (0, 0))
            self.imgs[ang] = img
        return self.imgs[ang]
class Pill(StackItem):
    img=imgx("Pill")
    name = "Pill"
    snd=sndget("drug")
    def stuse(self,tars,world,tx,ty,p):
        p.add_effect("Fast")
        self.snd.play()
        return True
class BridgeBuilder(StackItem):
    img=imgx("BridgeItem")
    name="Bridge"
    def stuse(self,tars,world,tx,ty,p):
        if not tars and not world.get_tclass(tx,ty).passable:
            world.change_t(tx,ty,5)
            return True
class GigaDrill(Item):
    img=imgx("GigaDrill")
    continuous = True
    def use(self,tars,world,tx,ty,p):
        dx,dy=D.get_dir(p.d)
        for n in range(1,4):
            gos=world.get_os(p.x+dx*n,p.y+dy*n)
            if not gos:
                break
            stop=False
            for o in gos:
                if not o.pick(world.w.get_sector(o)):
                    stop=True
                    break
            if stop:
                break
class Shield(Item):
    img=imgx("Shield")
    name="Shield"
class BOLReturn(Item):
    img=imgx("BOHOut")
    def use(self,tars,world,tx,ty,p):
        p.iinv=None
class BagOfLoot(Item):
    img=imgx("BOH")
    name = "BagLoot"
    def __init__(self):
        self.inv=[BOLReturn()]
    def add_item(self,item):
        if item.value:
            return True
class Flag(Item):
    img=imgx("Flag")
    name="Flag"
    def __init__(self,col,home):
        self.img=colcopy(self.img,(128,128,128),col)
        self.home=home
    def on_destroy(self):
        self.home.flag=self
        self.home.re_img()