__author__ = 'NoNotCar'
import pygame, sys
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1920,1080),pygame.FULLSCREEN|pygame.HWACCEL)
import Img
from random import choice
import Controllers
import World
import Players
Img.musplay("Party")
pdf = pygame.font.get_default_font()
tfont=pygame.font.Font(pdf,60)
sfont=pygame.font.Font(pdf,20)
clock = pygame.time.Clock()
tickimg=Img.img4("Tick")
crossimg=Img.img4("Null")
cols=((255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255),(255,128,0),(255,128,255))
sps=((1,1),(14,1),(1,14))
pimgs=[Img.create_man(col)[2] for col in cols]
breaking = False
#Img.musplay("ChOrDs.ogg")
def check_exit(event):
    if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
        sys.exit()
while not breaking:
    for event in pygame.event.get():
        check_exit(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            breaking = True
    screen.fill((255, 0, 0))
    Img.bcentre(tfont,"DUNGEON",screen)
    Img.bcentre(sfont,"Click to start",screen,50)
    pygame.display.flip()
    clock.tick(60)
breaking=False
controllers=[Controllers.Keyboard1(),Controllers.Keyboard2()]+[Controllers.UniJoyController(n) for n in range(pygame.joystick.get_count())]
activecons=[]
acps=[]
rsps=[]
rsc=[]
while not breaking:
    gevents=pygame.event.get()
    for event in gevents:
        check_exit(event)
        if event.type == pygame.MOUSEBUTTONDOWN and len(rsps):
            breaking = True
    for n,c in enumerate(activecons):
        if c.get_buttons(gevents)[0]:
            if acps[n] not in rsps:
                rsps.append(acps[n])
                rsc.append(c)
    for c in controllers[:]:
        if c.get_buttons(gevents)[0]:
            activecons.append(c)
            acps.append(0)
            controllers.remove(c)
    screen.fill((0, 0, 0))
    Img.bcentrex(tfont,"PLAYER SELECT",screen,0,(255,255,255))
    n=-1
    for n,c in enumerate(activecons):
        if c not in rsc:
            cdir=c.get_dir_pressed(gevents)
            if (1,0) == cdir:
                acps[n]=(acps[n]+1)%len(pimgs)
            elif (-1,0) == cdir:
                acps[n]=(acps[n]-1)%len(pimgs)
            Img.cxblit(pimgs[acps[n]],screen,n*64+94)
            if acps[n] in rsps:
                Img.cxblit(crossimg,screen,n*64+94,64)
        else:
            Img.cxblit(pimgs[acps[n]],screen,n*64+94)
            Img.cxblit(tickimg,screen,n*64+94,64)
    Img.bcentrex(sfont,"Press <use> to join",screen,n*64+160,(255,255,255))
    pygame.display.flip()
    clock.tick(60)
players=[Players.Player(sps[n][0],sps[n][1], cols[rsps[n]], activecons[n]) for n in range(len(activecons))]
w=World.World(players)
superrect=pygame.Rect(0,0,896,1032)
superrect.centerx=screen.get_rect().centerx
superrect.centery=screen.get_rect().centery
supersurf=screen.subsurface(superrect)
subsurfs=[supersurf.subsurface(pygame.Rect(n%2*448,n//2*516,448,516)) for n in range(4)]
screen.fill((100,100,100))
pygame.display.flip()
while True:
    es=pygame.event.get()
    for e in es:
        check_exit(e)
    screen.fill((0,0,0))
    w.update(es)
    for n,p in enumerate(players):
        w.render(p,subsurfs[n])
    pygame.display.update(superrect)
    clock.tick(60)
