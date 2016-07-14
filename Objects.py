from BaseClasses import Object, MultiPart
from Img import breakimgs, img4, sndget
import Items
breaksnd=sndget("break")
csh=sndget("cash")
class Wall(Object):
    o3d = 4
    imgs=breakimgs("Rock")
    blevel=0
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
    def __init__(self,x,y,world):
        self.place(x,y)
        for dx,dy in ((0,1),(1,0),(1,1)):
            tx=x+dx
            ty=y+dy
            world.spawn(MultiPart(tx,ty,self))
    def interact(self,world,p):
        item=p.inv[p.isel]
        if item.value:
            csh.play()
            p.remove_item(item)
            p.cash+=item.value
class Diamond(Object):
    img=img4("Diamond")
    def interact(self,world,p):
        if p.add_item(Items.Diamond()):
            world.dest(self)