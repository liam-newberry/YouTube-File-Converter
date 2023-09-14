# File created by: Liam Newberry

# External imports
import os
import pygame as pg
import pyperclip
# Internal imports
import file_funcs as ff
import draw_funcs as df
from settings import *

class Main:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.logo_image = pg.image.load(os.path.join(MAIN_FOLDER,"logo.png")).convert()
        self.logo_image.set_colorkey(GREEN)
        pg.display.set_caption(TITLE)
        pg.display.set_icon(self.logo_image)
    def new(self):
        self.screen_list = [self.paste_screen]
    def events(self):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                mouse_coords = pg.mouse.get_pos()
                if self.paste_screen in self.screen_list:
                    if self.paste_button_rect.collidepoint(mouse_coords):
                        self.clipboard_text = pyperclip.paste()
                        if VALID_URL not in self.clipboard_text:
                            self.screen_list.append(self.invalid_url_message)
                            self.invalid_url_time = self.now
                        else:
                            self.screen_list = [self.file_screen]
                            continue
                if self.file_screen in self.screen_list:
                    if self.mp3_rect.collidepoint(mouse_coords):
                        self.screen_list.append(self.loading_message)
                        self.draw()
                        ff.download_MP3(self.clipboard_text)
                        os.startfile(OUTPUT_FOLDER)
                        self.screen_list = [self.complete_screen]
                        continue
                    elif self.mp4_rect.collidepoint(mouse_coords):
                        self.screen_list = [self.res_screen]
                        continue
                if self.res_screen in self.screen_list:
                    res = None
                    if self.p360_rect.collidepoint(mouse_coords):
                        res = "360p"
                    elif self.p720_rect.collidepoint(mouse_coords):
                        res = "720p"
                    elif self.p1080_rect.collidepoint(mouse_coords):
                        res = "1080p"
                    if res != None:
                        self.screen_list.append(self.loading_message)
                        self.draw()
                        ff.download_MP4(self.clipboard_text,res)
                        os.startfile(OUTPUT_FOLDER)
                        self.screen_list = [self.complete_screen]
                        continue
                if self.complete_screen in self.screen_list:
                    if self.do_another_rect.collidepoint(mouse_coords):
                        self.new()
            if event.type == pg.QUIT:
                self.playing = False
    def paste_screen(self):
        self.paste_button_rect = df.draw_button(self,"Paste URL",(WIDTH/2,BUTTON_HEIGHT))
    def invalid_url_message(self):
        if self.now - self.invalid_url_time > 2500:
            self.invalid_url_time = 0
            self.screen_list.remove(self.invalid_url_message)
        df.draw_text(self.screen,"Invalid URL",(WIDTH/2,HEIGHT-10),FONT_SIZE,RED,"midbottom")
    def file_screen(self):
        self.mp3_rect = df.draw_button(self,"MP3",(WIDTH/3,BUTTON_HEIGHT))
        self.mp4_rect = df.draw_button(self,"MP4",(2*WIDTH/3,BUTTON_HEIGHT))
    def res_screen(self):
        self.p360_rect = df.draw_button(self,"360p",(WIDTH/5,BUTTON_HEIGHT))
        self.p720_rect = df.draw_button(self,"720p",(WIDTH/2,BUTTON_HEIGHT))
        self.p1080_rect = df.draw_button(self,"1080p",(4*WIDTH/5,BUTTON_HEIGHT))
    def loading_message(self):
        df.draw_text(self.screen,'Loading...',[WIDTH/2, HEIGHT-10],
                  FONT_SIZE,RED,"midbottom")
    def complete_screen(self):
        df.draw_text(self.screen,"Complete!",[WIDTH/2,HEIGHT/3],FONT_SIZE,RED,"midtop")
        self.do_another_rect = df.draw_button(self,"Do another",(WIDTH/2,(2*HEIGHT/3)+3))
    def update(self):
        self.now = pg.time.get_ticks()
    def draw(self):
        self.screen.fill(PRIMARY_COLOR)
        df.draw_text(self.screen,TITLE,[WIDTH/2,20],FONT_SIZE,RED,"midtop")
        for screen in self.screen_list:
            screen()
        pg.display.flip()
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
def main():
    m = Main()
    m.new()
    m.run()
    pg.quit()

main()