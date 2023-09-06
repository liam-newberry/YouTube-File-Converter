# File created by: Liam Newberry

# External imports
import os
import pygame as pg
import pyperclip
# Internal imports
from file_funcs import *
from draw_funcs import *
from settings import *
    
class Main:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        pg.display.set_caption("YouTube File Converter")
        self.logo_image = pg.image.load(os.path.join(main_folder,"logo.png")).convert()
        self.logo_image.set_colorkey(GREEN)
        pg.display.set_icon(self.logo_image)
    def new(self):
        self.draw_paste = True
        self.invalid_url = False
        self.invalid_url_time = 0
        self.draw_file_t= False
        self.clipboard_text = None
        self.loading_message = False
        self.mp3_rect = None
        self.mp4_rect = None
        self.res_choice = False
        self.p360_rect = None
        self.p720_rect = None
        self.p1080_rect = None
        self.complete = False
    def events(self):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                if self.draw_paste and self.paste_button_rect.collidepoint(pos):
                    self.clipboard_text = pyperclip.paste()
                    if "https://www.youtube.com/watch?v" not in self.clipboard_text:
                        self.clipboard_text = None
                        self.invalid_url = True
                        self.invalid_url_time = self.now
                    else:
                        self.draw_paste = False
                        self.draw_file_t = True
                        continue
                if self.draw_file_t:
                    if self.mp3_rect.collidepoint(pos):
                        self.draw(True)
                        download_MP3(self.clipboard_text)
                        os.startfile(main_folder + "/Outputs")
                        self.draw_file_t = False
                        self.complete = True
                        continue
                    elif self.mp4_rect.collidepoint(pos):
                        self.res_choice = True
                        self.draw_file_t = False
                        continue
                if self.res_choice:
                    res = None
                    if self.p360_rect.collidepoint(pos):
                        res = "360p"
                    elif self.p720_rect.collidepoint(pos):
                        res = "720p"
                    elif self.p1080_rect.collidepoint(pos):
                        res = "1080p"
                    if res != None:
                        self.draw(True)
                        download_MP4(self.clipboard_text,res)
                        os.startfile(main_folder + "/Outputs")
                        self.res_choice = False
                        self.complete = True
                        continue
                if self.complete:
                    if self.do_another_rect.collidepoint(pos):
                        self.new()
            if event.type == pg.QUIT:
                self.quit_window()
    def quit_window(self):
        if self.playing:
            self.playing = False
        self.running = False
        self.should_quit = True
    def draw_paste_button(self):
        text_rect = draw_text(self.screen,"Paste URL",(WIDTH/2,600),80,BLACK,"center",draw=False)
        size = [text_rect[2]+30,text_rect[3]+10]
        self.paste_button_rect = pg.Rect(draw_round_rect(self.screen,RED,10,[text_rect[0]-15,(HEIGHT/2)-5],size))
        draw_text(self.screen,"Paste URL",(WIDTH/2,(HEIGHT/2)+3),80,BLACK,"midtop")
    def draw_invalid_url(self):
        if self.invalid_url:
            if self.now - self.invalid_url_time > 2500:
                self.invalid_url_time = 0
                self.invalid_url = False
            draw_text(self.screen,"Invalid URL",(WIDTH/2,HEIGHT-10),FONT_SIZE,RED,"midbottom")
    def draw_file_type(self):
        text_rect = draw_text(self.screen,"MP3",(WIDTH/3,(HEIGHT/2)+3),80,BLACK,"center",draw=False)
        size = [text_rect[2]+30,text_rect[3]+10]
        self.mp3_rect = pg.Rect(draw_round_rect(self.screen,RED,10,[text_rect[0]-15,(HEIGHT/2)-5],size))
        draw_text(self.screen,"MP3",(WIDTH/3,(HEIGHT/2)+3),80,BLACK,"midtop")
        text_rect = draw_text(self.screen,"MP4",(2*WIDTH/3,(HEIGHT/2)+3),80,BLACK,"center",draw=False)
        size = [text_rect[2]+30,text_rect[3]+10]
        self.mp4_rect = pg.Rect(draw_round_rect(self.screen,RED,10,[text_rect[0]-15,(HEIGHT/2)-5],size))
        draw_text(self.screen,"MP4",(2*WIDTH/3,(HEIGHT/2)+3),80,BLACK,"midtop")
    def draw_res_select(self):
        text_rect = draw_text(self.screen,"360p",(WIDTH/5,(HEIGHT/2)+3),80,BLACK,"center",draw=False)
        size = [text_rect[2]+30,text_rect[3]+10]
        self.p360_rect = pg.Rect(draw_round_rect(self.screen,RED,10,[text_rect[0]-15,(HEIGHT/2)-5],size))
        draw_text(self.screen,"360p",(WIDTH/5,(HEIGHT/2)+3),80,BLACK,"midtop")
        text_rect = draw_text(self.screen,"720p",(2*WIDTH/4,(HEIGHT/2)+3),80,BLACK,"center",draw=False)
        size = [text_rect[2]+30,text_rect[3]+10]
        self.p720_rect = pg.Rect(draw_round_rect(self.screen,RED,10,[text_rect[0]-15,(HEIGHT/2)-5],size))
        draw_text(self.screen,"720p",(2*WIDTH/4,(HEIGHT/2)+3),80,BLACK,"midtop")
        text_rect = draw_text(self.screen,"1080p",(4*WIDTH/5,(HEIGHT/2)+3),80,BLACK,"center",draw=False)
        size = [text_rect[2]+30,text_rect[3]+10]
        self.p1080_rect = pg.Rect(draw_round_rect(self.screen,RED,10,[text_rect[0]-15,(HEIGHT/2)-5],size))
        draw_text(self.screen,"1080p",(4*WIDTH/5,(HEIGHT/2)+3),80,BLACK,"midtop")
    def draw_complete(self):
        draw_text(self.screen,"Complete!",[WIDTH/2,HEIGHT/3],80,RED,"midtop")
        text_rect = draw_text(self.screen,"Do another",(WIDTH/2,600),80,BLACK,"center",draw=False)
        size = [text_rect[2]+30,text_rect[3]+10]
        self.do_another_rect = pg.Rect(draw_round_rect(self.screen,RED,10,
                                                       [text_rect[0]-15,(2*HEIGHT/3)-5],size))
        draw_text(self.screen,"Do another",(WIDTH/2,(2*HEIGHT/3)+3),FONT_SIZE,BLACK,"midtop")
    def update(self):
        self.now = pg.time.get_ticks()
    def draw(self,loading:bool=False):
        self.screen.fill(PRIMARY_COLOR)
        draw_text(self.screen,"YouTube File Converter",[WIDTH/2,20],FONT_SIZE,RED,"midtop")
        if loading:
            draw_text(self.screen,'Loading...',[WIDTH/2, HEIGHT-10],FONT_SIZE,
                                    RED,"midbottom")
        if self.draw_paste:
            self.draw_paste_button()
        if self.invalid_url:
            self.draw_invalid_url()
        if self.draw_file_t:
            self.draw_file_type()
        if self.res_choice:
            self.draw_res_select()
        if self.complete:
            self.draw_complete()
        pg.display.flip()
    def run(self):
        self.should_quit = False
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        return self.should_quit
    
def main():
    m = Main()
    m.new()
    m.run()
    pg.quit()

main()