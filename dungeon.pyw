__author__ = 'NoNotCar'
import pygame, sys
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1920,1080),pygame.FULLSCREEN|pygame.HWACCEL)
import Img
import Controllers
import World
import Players
import GameModes
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
cgamemode=Img.button("STANDARD",sfont)
gamemodes=Img.button("GAME MODES",sfont)
gm=GameModes.gamemodes[0]
tutbutton=Img.button("TUTORIAL",sfont)
brects=[]
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
def selgamemode(screen):
    screen.fill((255,0,0))
    Img.bcentrex(tfont,"Select Gamemode",screen,0)
    brects=[]
    for n,gm in enumerate(GameModes.gamemodes):
        button=Img.button(gm.name,sfont)
        brects.append(Img.cxblit(button,screen,100+n*64))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            check_exit(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx,my=pygame.mouse.get_pos()
                for n,br in enumerate(brects):
                    if br.collidepoint(mx,my):
                        return GameModes.gamemodes[n]
while not breaking:
    for event in pygame.event.get():
        check_exit(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx,my=pygame.mouse.get_pos()
            if pygame.Rect(864,700,192,64).collidepoint(mx,my):
                mx-=864
                tsel=mx//64
            else:
                for n,br in enumerate(brects):
                    if br.collidepoint(mx,my):
                        if n==2:
                            tutorial(screen)
                        elif n:
                            gm=selgamemode(screen)
                            cgamemode=Img.button(gm.name,sfont)
                        else:
                            breaking = True
    screen.fill((255, 0, 0))
    brects=[]
    Img.bcentre(tfont,"TRAP DUNGEON",screen,-100)
    Img.bcentrex(sfont,"TIME:",screen,700)
    Img.cxblit(tselimgs[tsel],screen,750)
    for n,b in enumerate([cgamemode,gamemodes,tutbutton]):
        brects.append(Img.cxblit(b,screen,500+n*64))
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
    if len(rsps)<gm.maxp:
        Img.bcentrex(sfont,"Press <use> to join",screen,n*64+160,(255,255,255))
    else:
        break
    pygame.display.flip()
    clock.tick(60)
    dj.update()
while True:
    players=[Players.Player(sps[n][0],sps[n][1], cols[rsps[n]], rsc[n],gm) for n in range(len(rsc))]
    World.makenoise()
    w=gm.world(players)
    if gm.largescreen:
        ss = len(players)
        superrect = pygame.Rect(0, 0, 896 * ss, 1032)
        superrect.centerx = screen.get_rect().centerx
        supersurf = screen.subsurface(superrect)
        subsurfs = [supersurf.subsurface(pygame.Rect(n*896,0,896,1032)) for n in range(ss)]
    else:
        ss = (len(players) + 1) // 2
        superrect = pygame.Rect(0, 0, 448 * ss, 1032)
        superrect.centerx = screen.get_rect().centerx
        supersurf = screen.subsurface(superrect)
        subsurfs = [supersurf.subsurface(pygame.Rect(n % ss * 448, n // ss * 516, 448, 516)) for n in range(ss * 2)]
    screen.fill((100,100,100))
    timerect=pygame.Rect(881,1024,159,56)
    timesurf=screen.subsurface(timerect)
    pygame.display.flip()
    time=0 if gm.timereverse else 18000*(tsel+1)
    while True:
        es=pygame.event.get()
        for e in es:
            check_exit(e)
        supersurf.fill((0,0,0))
        w.update(es)
        for n,p in enumerate(players):
            if gm.largescreen:
                w.large_render(p,subsurfs[n])
            else:
                w.render(p,subsurfs[n])
        if time<0 and not gm.timereverse:
            break
        else:
            time+=1 if gm.timereverse else -1
        if gm.timereverse:
            if w.is_done():
                break
        timesurf.fill((255,255,255))
        Img.bcentrex(tfont,format_time(time),screen,1000,xoffset=4)
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

