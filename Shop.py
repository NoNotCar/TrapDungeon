from Img import imgx
class Shop(object):
    items=[]
    title="SHOP"
    def __init__(self,items,name="SHOP"):
        self.items=items
        self.title=name
class GPUpgrade(object):
    name="Upgrade"
    img=imgx("GPUpgrade")
    def upgrade(self,p):
        for i in p.inv:
            if i.name=="Pickaxe" and not i.golden:
                i.golden=True
                return True
class SpeedUpgrade(object):
    name="Upgrade"
    img=imgx("SpeedUpgrade")
    def upgrade(self,p):
        if p.defaultspeed<8:
            p.defaultspeed+=1
            return True
