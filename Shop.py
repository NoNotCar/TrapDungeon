from Img import img4
class Shop(object):
    items=[]
    def __init__(self,items):
        self.items=items
class GPUpgrade(object):
    name="Upgrade"
    img=img4("GPUpgrade")
    def upgrade(self,p):
        for i in p.inv:
            if i.name=="Pickaxe":
                i.golden=True
                return True
class SpeedUpgrade(object):
    name="Upgrade"
    img=img4("SpeedUpgrade")
    def upgrade(self,p):
        if p.defaultspeed<8:
            p.defaultspeed+=1
            return True
