from BaseClasses import Object
from Img import imgstrip4, imgstrip4f
import pygame
import Objects
class Enemy(Object):
    enemy = True
    loot=None
    def die(self,aworld):
        if self.loot is not None:
            aworld.spawn(self.loot(self.x,self.y))
class Ghost(Enemy):
    imgs = imgstrip4("Ghost")
    img = imgs[0]
    anitick = 0
    updates=True
    orect = pygame.Rect(16, 28, 32, 24)
    enemy=True
    speed = 2
    loot = Objects.Ruby
    def update(self, world, events):
        if self.anitick == 31:
            self.anitick = 0
            np = world.get_nearest_player(self.x, self.y)
            if np[1]<10:
                p=np[0]
                if p.x < self.x:
                    self.move(-1, 0, world)
                elif p.x > self.x:
                    self.move(1, 0, world)
                elif p.y > self.y:
                    self.move(0, 1, world)
                elif p.y < self.y:
                    self.move(0, -1, world)
        else:
            self.anitick += 1
        self.img = self.imgs[self.anitick // 8]
class AGhost(Ghost):
    imgs = imgstrip4("AngryGhost")
    anitick = 0
    sleepy=True
    updates=True
    orect = pygame.Rect(16, 28, 32, 24)
    enemy=True
    speed = 4
    tunneling=False
    loot = Objects.RedDiamond
    def update(self, world, events):
        if self.tunneling:
            gos=world.get_os(*self.tunneling)
            for o in gos[:]:
                o.pick(world.w.get_sector(o),1)
                if o not in gos:
                    self.tunneling=False
        if self.anitick == 15:
            if self.sleepy:
                np = world.get_nearest_player(self.x, self.y)
                if np[1]<=3:
                    self.sleepy=False
                    self.target=np[0]
            else:
                p=self.target
                if p.dead:
                    self.sleepy=True
                else:
                    if p.x < self.x:
                        self.amove(-1, 0, world)
                    elif p.x > self.x:
                        self.amove(1, 0, world)
                    elif p.y > self.y:
                        self.amove(0, 1, world)
                    elif p.y < self.y:
                        self.amove(0, -1, world)
            self.anitick = 0
        else:
            self.anitick += 1
    def get_img(self,world):
        if self.sleepy:
            return self.imgs[0]
        else:
            return self.imgs[self.anitick//4+1]
    def amove(self,dx,dy,world):
        if self.move(dx,dy,world):
            self.tunneling=False
            return None
        self.tunneling=(self.x+dx,self.y+dy)
class AngryWall(Objects.Wall):
    imgs=imgstrip4f("ExpRock",16)
    anitick=0
    updates = True
    def update(self,world,events):
        if self.anitick:
            self.anitick+=1
            if self.anitick==121:
                world.dest(self)
                world.create_exp(self.x,self.y,3,"Square")
        elif world.get_nearest_player(self.x,self.y)[1]==1:
            self.anitick=1
    def get_img(self,world):
        return self.imgs[(self.anitick+19)//20]
    def pick(self,world,strength=1):
        pass