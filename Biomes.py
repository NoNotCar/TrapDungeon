import Objects
import Enemies
from random import randint
class Biome(object):
    wall=None
    floor=0
    def GenerateWall(self,x,y,sector):
        sector.spawn(self.wall(x,y))
    def GenerateSpace(self,x,y,sector,noise):
        pass
class Cave(Biome):
    wall = Objects.Wall
    def GenerateWall(self,x,y,sector):
        if randint(0,25):
            sector.spawn(self.wall(x,y))
        elif randint(0,1):
            sector.spawn(Enemies.AngryWall(x,y))
        else:
            sector.spawn(Objects.GoldOre(x,y))
    def GenerateSpace(self,x,y,sector,noise):
        if not randint(0,50) and sector.d>=3:
            sector.spawn((Enemies.Spaceship if randint(0,5) else Enemies.AGhost)(x,y))
        elif not randint(0,50):
            sector.spawn(Objects.Diamond(x,y))
class Snow(Biome):
    wall = Objects.IceWall
    floor = 2
    def GenerateSpace(self,x,y,sector,noise):
        if not randint(0,50) and sector.d>=3:
            sector.spawn((Enemies.Thump if randint(0,2) else Enemies.IGhost)(x,y))
        elif not randint(0,50):
            sector.spawn(Objects.Diamond(x,y))
class Ice(Biome):
    wall = Objects.IceWall
    floor = 2
    def GenerateSpace(self,x,y,sector,noise):
        if randint(0,1):
            sector.change_t(x,y,6)
        if not randint(0,50) and sector.d>=3:
            sector.spawn((Enemies.Thump if randint(0,2) else Enemies.IGhost)(x,y))
        elif not randint(0,50):
            sector.spawn(Objects.Diamond(x,y))
class Volcanic(Biome):
    floor = 3
    def GenerateSpace(self,x,y,sector,noise):
        if noise>1.5 and randint(0,4):
            sector.change_t(x,y,4)
            if not randint(0,15) and sector.d>=3:
                sector.spawn(Enemies.FireElemental(x,y))
        elif not randint(0,25):
            sector.spawn(Objects.RedDiamond(x,y))
        elif not randint(0,25) and sector.d>=3:
            sector.spawn(Enemies.Ghost(x,y))
    def GenerateWall(self,x,y,sector):
        if randint(0,1):
            sector.spawn((Objects.DarkObsidian if randint(0,200) else Objects.InsaniumOre)(x,y))
        else:
            sector.spawn(Objects.Obsidian(x,y))
biomes=[Ice(),Snow(),Cave(),Volcanic()]
def convert(noise):
    return biomes[0] if noise>0.7 else biomes[1] if noise>0.4 else biomes[2] if noise>-0.4 else biomes[3]