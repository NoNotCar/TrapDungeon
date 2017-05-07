__author__ = 'NoNotCar'
import pygame
import os
from random import choice

np = os.path.normpath
loc = os.getcwd() + "/Assets/"
pygame.mixer.init()
teamcolours=((255,0,0),(0,0,255))
class ScaledImage(object):
    def __init__(self,img):
        if isinstance(img,list):
            self.imgs=img
            self.img=img[0]
        else:
            self.imgs=(img,)+tuple(xn(img,n) for n in (2,3,4))
            self.img=img
        self.h,self.w=self.img.get_height(),self.img.get_width()
    def blit(self,other,tpos,**kwargs):
        for n,i in enumerate(self.imgs):
            i.blit(other.imgs[n],(tpos[0]*(n+1),tpos[1]*(n+1)),**kwargs)
    def copy(self):
        return ScaledImage(self.img.copy())
    def __getitem__(self, item):
        return self.imgs[item]
def convertx(i):
    return i.convert_alpha()
    """px=pygame.PixelArray(i)
    for p in px:
        for n in p:
            if i.unmap_rgb(n)[3]!=255:
                del px
                return i.convert_alpha()
    else:
        del px
        return i.convert()"""
def img(fil):
    return convertx(pygame.image.load(np(loc + fil + ".png")))
def imgx(fil):
    i=img(fil)
    return ScaledImage(i)
def imgn(fil,n):
    return xn(img(fil),n)
def xn(img,n):
    return pygame.transform.scale(img,(int(img.get_width()*n),int(img.get_height()*n))).convert_alpha()
def ftrans(f,folder):
    return lambda x: f(folder+"/"+x)
def imgsz(fil, sz):
    return pygame.transform.scale(pygame.image.load(np(loc + fil + ".png")), sz).convert_alpha()

def imgstripx(fil):
    i = img(fil)
    imgs = []
    h=i.get_height()
    for n in range(i.get_width() // h):
        imgs.append(ScaledImage(i.subsurface(pygame.Rect(n * h, 0, h, h))))
    return imgs
def imgstrip(fil):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    h=img.get_height()
    for n in range(img.get_width() // h):
        imgs.append(img.subsurface(pygame.Rect(n * h, 0, h, h)).convert_alpha())
    return imgs
def imgstripxf(fil,w):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    h=img.get_height()
    for n in range(img.get_width() // w):
        imgs.append(ScaledImage(img.subsurface(pygame.Rect(n * w, 0, w, h))))
    return imgs
def imgstripxfs(fil,ws):
    i = img(fil)
    imgs = []
    h = i.get_height()
    cw=0
    for w in ws:
        imgs.append(ScaledImage(i.subsurface(pygame.Rect(cw, 0, w, h))))
        cw+=w
    return imgs
def imgrot(i,r=4):
    imgs=[i]
    for n in range(r-1):
        imgs.append(ScaledImage(pygame.transform.rotate(i[0],-90*n-90)))
    return imgs
def imgstriprot(fil,r=4):
    return [imgrot(i,r) for i in imgstripx(fil)]
def irot(i,n):
    return ScaledImage(pygame.transform.rotate(i.img,-90*n))
def bcentre(font, text, surface, offset=0, col=(0, 0, 0), xoffset=0):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.centerx = surface.get_rect().centerx + xoffset
    textrect.centery = surface.get_rect().centery + offset
    return surface.blit(render, textrect)

def bcentrex(font, text, surface, y, col=(0, 0, 0), xoffset=0):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.centerx = surface.get_rect().centerx + xoffset
    textrect.top = y
    return surface.blit(render, textrect)
def bcentrerect(font, text, surface, rect, col=(0, 0, 0)):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.centerx = rect.centerx
    textrect.centery = rect.centery
    return surface.blit(render, textrect)
def cxblit(source, dest, y, xoff=0):
    srect=source.get_rect()
    drect=dest.get_rect()
    srect.centerx=drect.centerx+xoff
    srect.top=y
    return dest.blit(source,srect)
def bcentrepos(font,text,surface,cpos,col=(0,0,0)):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.center=cpos
    return surface.blit(render, textrect)
def sndget(fil):
    return pygame.mixer.Sound(np(loc+"Sounds/"+fil+".wav"))

def hflip(img):
    return ScaledImage(pygame.transform.flip(img.img,1,0))
def ixn(img,n):
    return pygame.transform.scale(img,(img.get_width()*n,img.get_height()*n))
def x4(img):
    return xn(img,4)
def colswap(img,sc,ec):
    if isinstance(img,pygame.Surface):
        px=pygame.PixelArray(img)
        px.replace(sc,ec)
    else:
        for i in img.imgs:
            px = pygame.PixelArray(i)
            px.replace(sc, ec)
    return img
def colcopy(i,sc,ec):
    i=i.imgs[0].copy()
    colswap(i,sc,ec)
    return ScaledImage(i)
def darker(col,fract=0.5):
    return tuple(int(c*fract) for c in col)
def lighter(col,fract=0.5):
    return tuple(int(c+(255-c)*fract) for c in col)
def multicolcopy(img,*args):
    img=colcopy(img,*args[0])
    for s,e in args[1:]:
        colswap(img,s,e)
    return img
def new_bot(fil, col):
    imgs=imgstripx(fil)
    for i in imgs:
        colswap(i,(128,128,128),col)
    return imgs

def fload(fil,sz=16):
    return pygame.font.Font(np(loc+fil+".ttf"),sz)
def create_man(col):
    imgs=imgstrip("Man")
    for i in imgs:
        pygame.draw.rect(i,col,pygame.Rect(5,8,6,7))
    return [ScaledImage(i) for i in imgs]
himg=img("ManSink")
def create_sinking_man(col):
    imgs=[blank16.copy() for _ in range(14)]
    for n,i in enumerate(imgs):
        sinksurf=i.subsurface(pygame.Rect(0,0,16,15))
        sinksurf.blit(himg,(0,n))
        pygame.draw.rect(sinksurf,col,pygame.Rect(5,8+n,6,7))
    return [ScaledImage(i) for i in imgs]
breakani=imgstripxf("Break",16)
def breakimgs(fil):
    bimg=imgx(fil)
    bimgs=[bimg]
    for ani in breakani:
        timg=bimg.copy()
        timg.blit(ani,(0,0))
        bimgs.append(timg)
    return bimgs
buttimg=imgx("MenuButton")[3]
def button(text,font):
    img=buttimg.copy()
    bcentre(font,text,img,-4)
    return img
# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawTextRect(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    rots=[]
    for i in image.imgs:
        orig_rect = i.get_rect()
        rot_image = pygame.transform.rotate(i, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rots.append(rot_image.subsurface(rot_rect).copy())
    return ScaledImage(rots)
def musplay(mus,loop=-1):
    if mus[:3]=="EMX":
        pygame.mixer.music.load(np(loc +"EMX/"+ mus[3:] + ".ogg"))
        pygame.mixer.music.play(loop)
    else:
        pygame.mixer.music.load(np(loc+"Music/" + mus + ".ogg"))
        pygame.mixer.music.play(loop)

blank=imgx("Trans")
blank16=blank[0]
emxs = os.listdir(np(loc+"EMX/"))
emix=[]
for emx in emxs:
    if emx[-4:] == ".ogg":
        emix.append("EMX"+emx[:-4])
class DJ(object):
    def __init__(self,stdmix):
        self.songs=emix if emix else stdmix
    def update(self):
        if not pygame.mixer.music.get_busy():
            musplay(choice(self.songs),1)

#dfont=fload("PressStart2P")