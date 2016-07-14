from Img import img4
class Item(object):
    img=None
    continuous=False
    value=0
    def get_img(self):
        return self.img
    def use(self,tar,world):
        pass
class Pickaxe(Item):
    img=img4("BasicPick")
    continuous = True
    def use(self,tar,world):
        tar.pick(world.w.get_sector(tar))
class Diamond(Item):
    img=img4("Diamond")
    value=50