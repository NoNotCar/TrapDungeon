from Img import img4, sndget, imgstrip4
pickup=sndget("pickup")
defuse=sndget("tronic")
class Item(object):
    img=None
    continuous=False
    value=0
    def get_img(self):
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
    def get_img(self):
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
    assert item.name=="Trap", "THAT ISN'T AVAILABLE SORRY"
    return Trap(item)
class Trap(Item):
    def __init__(self,trapc):
        self.t=trapc
    def get_img(self):
        return self.t.img
    def use(self,tars,world,tx,ty,p):
        if not tars:
            world.spawn(self.t(tx,ty))
        p.remove_item(self)
        pickup.play()