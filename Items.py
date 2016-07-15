from Img import img4, sndget
pickup=sndget("pickup")
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
    img=img4("Defuser")
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