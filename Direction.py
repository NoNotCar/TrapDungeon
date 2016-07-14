import pygame
directions=((0,-1),(1,0),(0,1),(-1,0))
kconv=(pygame.K_w,pygame.K_d,pygame.K_s,pygame.K_a)
vert=((0,-1),(0,1))
hoz=((1,0),(-1,0))
def rotdir(d,x):
    return directions[(directions.index(d)+x)%4]
def anti(d):
    return rotdir(d,2)
def get_dir(x):
    return directions[x%4]
def index(d):
    return directions.index(d)
def offset(d,e):
    dire=get_dir(d)
    return e.x+dire[0],e.y+dire[1]