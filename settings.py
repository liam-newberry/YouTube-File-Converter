# File created by: Liam Newberry

# External imports
import os

# os
MAIN_FOLDER = os.getcwd()
OUTPUT_FOLDER = MAIN_FOLDER + "/Outputs"
# window
FPS = 10
WIDTH = 700
HEIGHT = 375
# colors
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
# graphics 
PRIMARY_COLOR = (10,10,10)
FONT_SIZE = 80
BUTTON_ROUNDNESS = 10
BUTTON_HEIGHT = (HEIGHT/2) + 3
# app 
TITLE = "YouTube File Converter"
VALID_URL = "https://www.youtube.com/watch?v"
ITAG_DICT = {"360p":18,
             "720p":22,
             "1080p":137}
MP3_ITAG = ITAG_DICT["360p"]