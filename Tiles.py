from Img import imgx
class Tile(object):
    img=None
    passable=True
    slippery=False
    def get_img(self):
        return self.img
class Floor(Tile):
    def __init__(self,imgname):
        self.img=imgx(imgname)
class Lava(Tile):
    passable = False
    img=imgx("Lava")
class Ice(Tile):
    img = imgx("Ice")
    slippery = True
tiles=[Floor("Floor"),Floor("Grass"),Floor("Snow"),Floor("ScorchedFloor"),Lava(),Floor("Bridge"),Ice(),Floor("BrickFloor"),Floor("Sand")]