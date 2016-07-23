import Img
import Direction as D
from random import randint, sample
from pygame import Rect
def dimg(fil):
    return  Img.img("DeathGame/"+fil)
pbase=dimg("Man")
skull=dimg("Skull")
coin=dimg("Coin")
dfont=Img.fload("cool",64)
sfont=Img.fload("cool",32)
pdie=Img.sndget("pdie")
csh=Img.sndget("cash")
drect=Rect(6,2,20,28)
prect=Rect(10,2,12,27)
crect=Rect(3,3,26,26)
class DeathGame(object):
    def __init__(self,p):
        self.mimg=pbase.copy()
        Img.colswap(self.mimg,(128,128,128),p.col)
        self.t=1200
        self.c=p.c
        self.p=p
        self.px=208
        self.objs=[]
    def update(self):
        self.t-=1
        if not self.t%60:
            rs=sample(range(14),6)
            for n,r in enumerate(rs):
                self.objs.append([not n,[r*32,-32]])
        for d in self.c.get_dirs():
            if d in D.hoz:
                if d==(1,0) and self.px<416:
                    self.px+=4
                elif d==(-1,0) and self.px>0:
                    self.px-=4
        for o in self.objs[:]:
            if o[1][1]<516:
                o[1][1]+=4
            else:
                self.objs.remove(o)
        for o in self.objs[:]:
            if prect.move(self.px,440).colliderect((crect if o[0] else drect).move(*o[1])):
                if o[0]:
                    self.p.cash+=2
                    csh.play()
                else:
                    self.t+=180
                    pdie.play()
                self.objs.remove(o)
    def render(self,screen):
        Img.bcentre(dfont,"DEAD",screen,-48,self.p.col)
        Img.bcentre(sfont,str(self.t//60+1),screen,col=self.p.col)
        screen.blit(self.mimg,(self.px,440))
        for o in self.objs:
            screen.blit((skull,coin)[o[0]],o[1])
