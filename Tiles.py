from Img import img4
class Tile(object):
    img=None
    passable=True
    def get_img(self):
        return self.img
class Floor(Tile):
    def __init__(self,imgname):
        self.img=img4(imgname)
tiles=[Floor("Floor")]