# File created by: Liam Newberry

# External imports
from moviepy.editor import AudioFileClip
from moviepy.editor import VideoFileClip
import os
import pytube
import shutil
# Internal imports
from settings import *

def combine_audio(video_path:str,audio_path:str):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)
    video_clip_with_audio = video_clip.set_audio(audio_clip)
    video_clip_with_audio.write_videofile("new.mp4")

def download_1080p(url:str):
    download_MP3(url,False)
    itag = ITAG_DICT["1080p"]
    video = pytube.YouTube(url)
    stream = video.streams.get_by_itag(itag)
    stream.download()
    filename = stream.default_filename
    mp3_file = filename[:-4] + ".mp3"
    vidpath = os.path.abspath(filename)
    audpath = os.path.abspath(mp3_file)
    combine_audio(vidpath,audpath)
    if os.path.exists(mp3_file):
        os.remove(mp3_file)
    if os.path.exists(filename):
        os.remove(filename)
    cur_path = MAIN_FOLDER + "/" + filename
    dest_path = MAIN_FOLDER + "/Outputs"
    temp_path = os.path.abspath("new.mp4")
    final_path = dest_path + "/" + filename
    os.rename(temp_path,cur_path)
    if not os.path.exists("Outputs"):
        os.makedirs("Outputs")
    if not os.path.exists(final_path):
        shutil.move(cur_path,dest_path)
    else:
        os.remove(final_path)
        shutil.move(cur_path,dest_path)

def download_MP3(url:str,move:bool=True):
    video = pytube.YouTube(url)
    stream = video.streams.get_by_itag(MP3_ITAG)
    stream.download()
    filename = stream.default_filename
    clip = VideoFileClip(filename)
    mp3_file = filename[:-4] + ".mp3"
    clip.audio.write_audiofile(mp3_file)
    clip.close()
    if os.path.exists(filename):
        os.remove(filename)
    if move:
        if not os.path.exists("Outputs"):
            os.makedirs("Outputs")
        cur_path = MAIN_FOLDER + "/" + mp3_file
        dest_path = MAIN_FOLDER + "/Outputs"
        if not os.path.exists(dest_path + "/" + mp3_file):
            shutil.move(cur_path,dest_path)
        else:
            os.remove(mp3_file)
        return mp3_file

def download_MP4(url:str,quality:str):
    if quality == "1080p":
        download_1080p(url)
        return None
    itag = ITAG_DICT[quality]
    video = pytube.YouTube(url)
    stream = video.streams.get_by_itag(itag)
    stream.download()
    filename = stream.default_filename
    if not os.path.exists("Outputs"):
        os.makedirs("Outputs")
    cur_path = MAIN_FOLDER + "/" + filename
    if os.path.exists(OUTPUT_FOLDER + "/" + filename):
        os.remove(OUTPUT_FOLDER + "/" + filename)
    shutil.move(cur_path,OUTPUT_FOLDER)