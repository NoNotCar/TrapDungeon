from Img import img4, sndget, imgstrip4
pickup=sndget("pickup")
defuse=sndget("tronic")
class Item(object):
    img=None
    continuous=False
    value=0
    def get_img(self,p):
        return self.img
    def use(self,tars,world,tx,ty,p):
        pass
class Pickaxe(Item):
    img=img4("BasicPick")
    continuous = True
    def use(self,tars,world,tx,ty,p):
        if tars:
            tars[0].pick(world.w.get_sector(tars[0]))
class Defuser(Item):
    imgs=imgstrip4("Defuser")
    cooldown=0
    def get_img(self,p):
        if self.cooldown:
            self.cooldown-=1
        return self.imgs[bool(self.cooldown)]
    def use(self,tars,world,tx,ty,p):
        if not self.cooldown:
            defuse.play()
            for dx in range(-3,4):
                for dy in range(-3,4):
                    for o in world.get_os(p.x+dx,p.y+dy):
                        if o.name=="Trap":
                            o.hidden=False
            self.cooldown=600
class Diamond(Item):
    img=img4("Diamond")
    value=50
def wrap(item):
    assert item.name in ["Trap", "Compass"], "THAT ISN'T AVAILABLE SORRY"
    if item.name=="Trap":
        return Trap(item)
    return Compass()
class Trap(Item):
    def __init__(self,trapc):
        self.t=trapc
    def get_img(self,p):
        return self.t.img
    def use(self,tars,world,tx,ty,p):
        if not tars:
            world.spawn(self.t(tx,ty))
        p.remove_item(self)
        pickup.play()
class Compass(Item):
    imgs=imgstrip4("Compass")
    name="Compass"
    img=imgs[0]
    def get_img(self,p):
        dx=p.x-7
        dy=p.y-7
        n=0
        if abs(dx)>abs(dy):
            if dx>0:
                n=3
            else:
                n=1
        else:
            if dy>0:
                n=0
            else:
                n=2
        return self.imgs[n]