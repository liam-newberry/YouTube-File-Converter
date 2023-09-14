# File created by: Liam Newberry

# External imports
import pygame as pg
# Internal imports
from settings import *

def draw_button(object:object,text:str,coordinates:tuple):
    text_rect = draw_text(object.screen,text,coordinates,FONT_SIZE,BLACK,"center",draw=False)
    size = [text_rect[2]+30,text_rect[3]+10]
    button_rect = pg.Rect(draw_round_rect(object.screen,RED,BUTTON_ROUNDNESS,
                                          [text_rect[0]-15,coordinates[1]-8],size))
    draw_text(object.screen,text,coordinates,FONT_SIZE,BLACK,"midtop")
    return button_rect

def draw_round_rect(surface:object,color:tuple,radius:int,coordinates:list,size:list):
    tl_coords = [coordinates[0]+radius,coordinates[1]+radius]
    tl_circ = pg.draw.circle(surface,color,tl_coords,radius)
    tr_coords = [coordinates[0]+size[0]-radius,coordinates[1]+radius]
    tr_circ = pg.draw.circle(surface,color,tr_coords,radius)
    bl_coords = [coordinates[0]+radius,coordinates[1]+size[1]-radius]
    bl_circ = pg.draw.circle(surface,color,bl_coords,radius)
    br_coords = [coordinates[0]+size[0]-radius,coordinates[1]+size[1]-radius]
    br_circ = pg.draw.circle(surface,color,br_coords,radius)
    l_rect_length = abs(tl_circ.x-tr_circ.x)+2*radius
    l_rect_width = abs(tl_circ.y-bl_circ.y)
    l_rect = pg.draw.rect(surface,color,[tl_circ.x,tl_circ.center[1],l_rect_length,l_rect_width])
    w_rect_length = abs(tl_circ.x-tr_circ.x)
    w_rect_width = abs(tl_circ.y-bl_circ.y)+2*radius
    w_rect = pg.draw.rect(surface,color,[tl_circ.center[0],tl_circ.y,w_rect_length,w_rect_width])
    return [coordinates[0],coordinates[1],size[0],size[1]]

def draw_text(surface:object,text:str,coordinates:list,pt:int,color:tuple=BLACK,
            align:str="topleft",font:str="ariel",bold:bool=False,italicize:bool=False,draw:bool=True):
    font_name = pg.font.match_font(font, bold, italicize)
    font = pg.font.Font(font_name, pt)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if align == "topleft":
        text_rect.topleft = coordinates
    elif align == "topright":
        text_rect.topright = coordinates
    elif align == "center":
        text_rect.center = coordinates
    elif align == "midtop":
        text_rect.midtop = coordinates
    elif align == "midbottom":
        text_rect.midbottom = coordinates
    elif align == "midleft":
        text_rect.midleft = coordinates
    elif align == "midright":
        text_rect.midright = coordinates
    elif align == "bottomleft":
        text_rect.bottomleft = coordinates
    elif align == "bottomright":
        text_rect.bottomright = coordinates
    if draw:
        surface.blit(text_surface, text_rect)
    return text_rect