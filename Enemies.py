from BaseClasses import Object
from Img import imgstrip4
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