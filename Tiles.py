from Img import img4
class Tile(object):
    img=None
    passable=True
    slippery=False
    def get_img(self):
        return self.img
class Floor(Tile):
    def __init__(self,imgname):
        self.img=img4(imgname)
class Lava(Tile):
    passable = False
    img=img4("Lava")
class Ice(Tile):
    img = img4("Ice")
    slippery = True
tiles=[Floor("Floor"),Floor("Grass"),Floor("Snow"),Floor("ScorchedFloor"),Lava(),Floor("Bridge"),Ice()]