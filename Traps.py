import BaseClasses
from Img import img4, blank64, sndget
trap=sndget("trap")
breaksnd=sndget("break")
class Trap(BaseClasses.Object):
    effect=None
    name="Trap"
    solid=False
    hidden=True
    def __init__(self,x,y,p):
        self.owner=p
        self.place(x,y)
    def walkover(self,p,world):
        p.add_effect(self.effect)
        world.dest(self)
        trap.play()
    def is_hidden(self,world,p):
        return p is not self.owner and self.hidden
    def pick(self,world,strength):
        if not self.hidden:
            world.dest(self)
            breaksnd.play()
class PauseTrap(Trap):
    img=img4("PauseTrap")
    effect = "Pause"
class SlowTrap(Trap):
    img=img4("SlowTrap")
    effect = "Slow"
class ReverseTrap(Trap):
    img=img4("ReverseTrap")
    effect = "Reverse"
