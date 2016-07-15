import pygame
import UniJoy
class Controller(object):
    def get_buttons(self,events):
        return 0,0,0
    def get_dirs(self):
        return [(0,0)]
    def get_pressed(self):
        return 0,0

class Keyboard1(Controller):
    kconv = {pygame.K_w: (0, -1), pygame.K_s: (0, 1), pygame.K_a: (-1, 0), pygame.K_d: (1, 0)}
    def get_buttons(self,events):
        bomb=False
        act=False
        lr=0
        for e in events:
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_SPACE:
                    bomb=True
                elif e.key==pygame.K_LSHIFT:
                    act=True
                elif e.key==pygame.K_q:
                    lr=-1
                elif e.key==pygame.K_e:
                    lr=1
        return bomb,act,lr
    def get_pressed(self):
        keys = pygame.key.get_pressed()
        return (keys[pygame.K_SPACE],keys[pygame.K_LSHIFT])
    def get_dirs(self):
        keys = pygame.key.get_pressed()
        kpr=[]
        for k, v in self.kconv.iteritems():
            if keys[k]:
                kpr.append(v)
        return kpr
    def get_dir_pressed(self,events):
        for e in events:
            if e.type==pygame.KEYDOWN and e.key in self.kconv.keys():
                return self.kconv[e.key]
class Keyboard2(Keyboard1):
    kconv={pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1), pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)}
    def get_buttons(self,events):
        bomb=False
        act=False
        lr=0
        for e in events:
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_RETURN:
                    bomb=True
                elif e.key==pygame.K_RCTRL:
                    act=True
                elif e.key==pygame.K_DELETE:
                    lr=-1
                elif e.key==pygame.K_PAGEDOWN:
                    lr=1
        return bomb,act,lr
    def get_pressed(self):
        keys = pygame.key.get_pressed()
        return (keys[pygame.K_RETURN],keys[pygame.K_RCTRL])
class UniJoyController(Controller):
    cooldown=0
    def __init__(self,n):
        self.uj=UniJoy.Unijoy(n)
    def get_buttons(self,events):
        bomb=False
        act=False
        lr=0
        for e in events:
            if e.type==pygame.JOYBUTTONDOWN and e.joy==self.uj.jnum:
                if self.uj.get_b("A"):
                    bomb=True
                if self.uj.get_b("B"):
                    act=True
                if self.uj.get_b("L1"):
                    lr=-1
                if self.uj.get_b("R1"):
                    lr=1
                break
        return bomb,act,lr
    def get_dirs(self):
        ds=self.uj.getdirstick(1)
        if ds!=(0,0):
            return [ds]
        return []
    def get_dir_pressed(self,events):
        ds=self.uj.getdirstick(1)
        if self.cooldown:
            self.cooldown-=1
            return 0,0
        else:
            if ds!=(0,0):
                self.cooldown=30
            return ds
    def get_pressed(self):
        return (self.uj.get_b("A"),self.uj.get_b("B"))