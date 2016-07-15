import BaseClasses
from Img import img4, blank64, sndget
trap=sndget("trap")
class Trap(BaseClasses.Object):
    effect=None
    name="Trap"
    solid=False
    def walkover(self,p,world):
        p.add_effect(self.effect)
        world.dest(self)
        trap.play()
    def get_img(self,world):
        return blank64
class PauseTrap(Trap):
    img=img4("PauseTrap")
    effect = "Pause"
class SlowTrap(Trap):
    img=img4("SlowTrap")
    effect = "Slow"
