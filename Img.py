__author__ = 'NoNotCar'
import pygame
import os
from random import choice

np = os.path.normpath
loc = os.getcwd() + "/Assets/"
pygame.mixer.init()
teamcolours=((255,0,0),(0,0,255))
def img(fil):
    return pygame.image.load(np(loc + fil + ".png")).convert_alpha()
def img4(fil):
    i=img(fil)
    return pygame.transform.scale(i,(i.get_width()*4,i.get_height()*4)).convert_alpha()

def imgsz(fil, sz):
    return pygame.transform.scale(pygame.image.load(np(loc + fil + ".png")), sz).convert_alpha()

def imgstrip4(fil):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    h=img.get_height()
    for n in range(img.get_width() // h):
        imgs.append(pygame.transform.scale(img.subsurface(pygame.Rect(n * h, 0, h, h)), (h*4, h*4)).convert_alpha())
    return imgs
def imgstrip(fil):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    h=img.get_height()
    for n in range(img.get_width() // h):
        imgs.append(img.subsurface(pygame.Rect(n * h, 0, h, h)).convert_alpha())
    return imgs
def imgstrip4f(fil,w):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    h=img.get_height()
    for n in range(img.get_width() // w):
        imgs.append(pygame.transform.scale(img.subsurface(pygame.Rect(n * w, 0, w, h)), (w*4, h*4)).convert_alpha())
    return imgs
def imgrot(i):
    imgs=[i]
    for n in range(3):
        imgs.append(pygame.transform.rotate(i,-90*n-90))
    return imgs


def musplay(fil,loops=-1):
    if fil[:3]=="EMX":
        pygame.mixer.music.load(np(loc+"EMX/" + fil[3:]+".ogg"))
    else:
        pygame.mixer.music.load(np(loc+"Music/" + fil+".ogg"))
    pygame.mixer.music.play(loops)


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
def colswap(img,sc,ec):
    px=pygame.PixelArray(img)
    px.replace(sc,ec)
def colcopy(i,sc,ec):
    i=i.copy()
    colswap(i,sc,ec)
    return i
def multicolcopy(img,*args):
    img=colcopy(img,*args[0][0])
    for s,e in args[0][1:]:
        colswap(img,s,e)
    return img
def sndget(fil):
    return pygame.mixer.Sound(np(loc+"Sounds/"+fil+".wav"))

def hflip(img):
    return pygame.transform.flip(img,1,0)

def x4(img):
    return pygame.transform.scale(img,(img.get_width()*4,img.get_height()*4))

def fload(fil,sz=16):
    return pygame.font.Font(np(loc+fil+".ttf"),sz)
def create_man(col):
    imgs=imgstrip4("Man")
    for i in imgs:
        pygame.draw.rect(i,col,pygame.Rect(20,32,24,28))
    return imgs
himg=img4("ManSink")
def create_sinking_man(col):
    imgs=[blank64.copy() for _ in range(14)]
    for n,i in enumerate(imgs):
        sinksurf=i.subsurface(pygame.Rect(0,0,64,60))
        sinksurf.blit(himg,(0,n*4))
        pygame.draw.rect(sinksurf,col,pygame.Rect(20,32+n*4,24,28))
    return imgs
breakani=imgstrip4f("Break",16)
def breakimgs(fil):
    bimg=img4(fil)
    bimgs=[bimg]
    for ani in breakani:
        timg=bimg.copy()
        timg.blit(ani,(0,0))
        bimgs.append(timg)
    return bimgs
buttimg=img4("MenuButton")
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
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

blank64=img4("Trans")
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