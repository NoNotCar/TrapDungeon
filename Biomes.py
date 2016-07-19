import Objects
import Enemies
from random import randint
class Biome(object):
    wall=None
    floor=0
    def GenerateWall(self,x,y,sector):
        sector.spawn(self.wall(x,y))
    def GenerateSpace(self,x,y,sector):
        pass
    def GenerateEx(self,sector):
        pass
class Cave(Biome):
    wall = Objects.Wall
    def GenerateWall(self,x,y,sector):
        if randint(0,50):
            sector.spawn(self.wall(x,y))
        else:
            sector.spawn(Enemies.AngryWall(x,y))
    def GenerateSpace(self,x,y,sector):
        if not randint(0,50) and sector.d>=3:
            sector.spawn((Enemies.Spaceship if randint(0,5) else Enemies.AGhost)(x,y))
class Snow(Biome):
    wall = Objects.IceWall
    floor = 2
    def GenerateSpace(self,x,y,sector):
        if not randint(0,50) and sector.d>=3:
            sector.spawn((Enemies.Ghost if randint(0,1) else Enemies.Thump)(x,y))
def convert(noise):
    return Cave() if noise<0.3 else Snow()