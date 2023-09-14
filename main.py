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
        self.draw_paste = "paste"
        self.draw_file_t = False
        self.res_choice = False
        self.complete = False
        self.invalid_url = False
        self.loading = False
        self.invalid_url_time = 0
        self.screen_dict = {"paste":self.paste_screen,
                            "file":self.file_screen,
                            "resolution":self.res_screen,
                            "complete":self.complete_screen,
                            "invalid":self.invalid_url_message,
                            "loading":self.loading_message}
    def events(self):
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                if self.draw_paste != False and self.paste_button_rect.collidepoint(pos):
                    self.clipboard_text = pyperclip.paste()
                    if VALID_URL not in self.clipboard_text:
                        self.clipboard_text = None
                        self.invalid_url = "invalid"
                        self.invalid_url_time = self.now
                    else:
                        self.draw_paste = False
                        self.draw_file_t = "file"
                        continue
                if self.draw_file_t:
                    if self.mp3_rect.collidepoint(pos):
                        self.loading = "loading"
                        self.update()
                        self.draw()
                        ff.download_MP3(self.clipboard_text)
                        os.startfile(OUTPUT_FOLDER)
                        self.loading = False
                        self.draw_file_t = False
                        self.complete = "complete"
                        continue
                    elif self.mp4_rect.collidepoint(pos):
                        self.res_choice = "resolution"
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
                        self.loading = "loading"
                        self.update()
                        self.draw()
                        ff.download_MP4(self.clipboard_text,res)
                        os.startfile(OUTPUT_FOLDER)
                        self.loading = False
                        self.res_choice = False
                        self.complete = "complete"
                        continue
                if self.complete:
                    if self.do_another_rect.collidepoint(pos):
                        self.new()
            if event.type == pg.QUIT:
                self.playing = False
            #     if self.draw_paste and self.paste_button_rect.collidepoint(pos):
            #         self.clipboard_text = pyperclip.paste()
            #         if VALID_URL not in self.clipboard_text:
            #             self.clipboard_text = None
            #             self.invalid_url = True
            #             self.invalid_url_time = self.now
            #         else:
            #             self.draw_paste = False
            #             self.draw_file_t = True
            #             continue
            #     if self.draw_file_t:
            #         if self.mp3_rect.collidepoint(pos):
            #             self.draw(True)
            #             ff.download_MP3(self.clipboard_text)
            #             os.startfile(OUTPUT_FOLDER)
            #             self.draw_file_t = False
            #             self.complete = True
            #             continue
            #         elif self.mp4_rect.collidepoint(pos):
            #             self.res_choice = True
            #             self.draw_file_t = False
            #             continue
            #     if self.res_choice:
            #         res = None
            #         if self.p360_rect.collidepoint(pos):
            #             res = "360p"
            #         elif self.p720_rect.collidepoint(pos):
            #             res = "720p"
            #         elif self.p1080_rect.collidepoint(pos):
            #             res = "1080p"
            #         if res != None:
            #             self.draw(True)
            #             ff.download_MP4(self.clipboard_text,res)
            #             os.startfile(OUTPUT_FOLDER)
            #             self.res_choice = False
            #             self.complete = True
            #             continue
            #     if self.complete:
            #         if self.do_another_rect.collidepoint(pos):
            #             self.new()
            # if event.type == pg.QUIT:
            #     self.playing = False
    def paste_screen(self):
        self.paste_button_rect = df.draw_button(self,"Paste URL",(WIDTH/2,BUTTON_HEIGHT))
    def invalid_url_message(self):
        if self.invalid_url:
            if self.now - self.invalid_url_time > 2500:
                self.invalid_url_time = 0
                self.invalid_url = False
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
        self.screen_list = [self.draw_paste,self.draw_file_t,self.res_choice,
                            self.complete,self.invalid_url,self.loading]
    def draw(self,loading:bool=False):
        self.screen.fill(PRIMARY_COLOR)
        df.draw_text(self.screen,TITLE,[WIDTH/2,20],FONT_SIZE,RED,"midtop")
        # if loading:
        #     self.loading_message()
        # if self.draw_paste:
        #     self.paste_screen()
        # if self.invalid_url:
        #     self.invalid_url_message()
        # if self.draw_file_t:
        #     self.file_screen()
        # if self.res_choice:
        #     self.res_screen()
        # if self.complete:
        #     self.complete_screen()
        for item in self.screen_list:
            if item != False:
                self.screen_dict[item]()
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