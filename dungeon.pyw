__author__ = 'NoNotCar'
import pygame, sys
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1920,1080),pygame.FULLSCREEN|pygame.HWACCEL)
import Img
import Controllers
import World
import Players
pdf = pygame.font.get_default_font()
tfont=Img.fload("cool",64)
sfont=Img.fload("cool",32)
clock = pygame.time.Clock()
tickimg=Img.img4("Tick")
crossimg=Img.img4("Null")
tselimgs=Img.imgstrip4f("TSelect",64)
tsel=0
cols=((255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255),(255,128,0),(255,128,255))
sps=((1,1),(14,1),(1,14),(14,14),(4,4),(11,4),(4,11),(11,11))
pimgs=[Img.create_man(col)[2] for col in cols]
tutimgs=[Img.img("T"+str(n)) for n in range(1,4)]
breaking = False
dj=Img.DJ(["Party"])
def format_time(time):
    t=time+60
    secs=t%3600//60
    if secs<10:
        secs="0"+str(secs)
    else:
        secs=str(secs)
    return str(t//3600)+":"+secs
def check_exit(event):
    if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
        sys.exit()
def tutorial(screen):
    for t in tutimgs:
        screen.blit(t,(0,0))
        pygame.display.flip()
        done=False
        while not done:
            for event in pygame.event.get():
                check_exit(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    done=True
while not breaking:
    for event in pygame.event.get():
        check_exit(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx,my=pygame.mouse.get_pos()
            if pygame.Rect(864,700,192,64).collidepoint(mx,my):
                mx-=864
                tsel=mx//64
            else:
                breaking = True
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_t:
            tutorial(screen)
    screen.fill((255, 0, 0))
    Img.bcentre(tfont,"TRAP DUNGEON",screen)
    Img.bcentre(sfont,"Click to start",screen,50)
    Img.bcentre(sfont,"Press T for Tutorial",screen,75)
    Img.bcentrex(sfont,"TIME:",screen,650)
    Img.cxblit(tselimgs[tsel],screen,700)
    pygame.display.flip()
    clock.tick(60)
    dj.update()
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
    dj.update()
while True:
    players=[Players.Player(sps[n][0],sps[n][1], cols[rsps[n]], rsc[n]) for n in range(len(rsc))]
    World.makenoise()
    w=World.World(players)
    ss=(len(players)+1)//2
    superrect=pygame.Rect(0,0,448*ss,1032)
    superrect.centerx=screen.get_rect().centerx
    supersurf=screen.subsurface(superrect)
    subsurfs=[supersurf.subsurface(pygame.Rect(n%ss*448,n//ss*516,448,516)) for n in range(ss*2)]
    screen.fill((100,100,100))
    timerect=pygame.Rect(881,1024,159,56)
    timesurf=screen.subsurface(timerect)
    pygame.display.flip()
    timeleft=18000*(tsel+1)
    while True:
        es=pygame.event.get()
        for e in es:
            check_exit(e)
        supersurf.fill((0,0,0))
        w.update(es)
        for n,p in enumerate(players):
            w.render(p,subsurfs[n])
        if timeleft<0:
            break
        else:
            timeleft-=1
        timesurf.fill((255,255,255))
        Img.bcentrex(tfont,format_time(timeleft),screen,1000,xoffset=4)
        pygame.display.update([superrect,timerect])
        clock.tick(60)
        dj.update()
    winscore=max([p.cash for p in players])
    screen.fill((100,100,100))
    supersurf.fill((0,0,0))
    for n,p in enumerate(players):
        Img.bcentre(tfont,"WIN" if p.cash==winscore else "LOSE",subsurfs[n],col=p.col)
    pygame.display.flip()
    pygame.time.wait(2500)

