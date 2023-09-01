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

def download_1080p(link:str):
    download_MP3(link,False)
    itag = 137
    video = pytube.YouTube(link)
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
    cur_path = main_folder + "/" + filename
    dest_path = main_folder + "/Outputs"
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

def download_MP3(link:str,move:bool=True):
    video = pytube.YouTube(link)
    stream = video.streams.get_by_itag(18)
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
        cur_path = main_folder + "/" + mp3_file
        dest_path = main_folder + "/Outputs"
        if not os.path.exists(dest_path + "/" + mp3_file):
            shutil.move(cur_path,dest_path)
        else:
            os.remove(mp3_file)
        return mp3_file

def download_MP4(link:str,quality:str):
    if quality == "1080p":
        download_1080p(link)
        return None
    itag_dict = {"360p":18,
                    "720p":22}
    itag = itag_dict[quality]
    video = pytube.YouTube(link)
    stream = video.streams.get_by_itag(itag)
    stream.download()
    filename = stream.default_filename
    if not os.path.exists("Outputs"):
        os.makedirs("Outputs")
    cur_path = main_folder + "/" + filename
    dest_path = main_folder + "/Outputs"
    if not os.path.exists(dest_path + "/" + filename):
        shutil.move(cur_path,dest_path)
    else:
        os.remove(dest_path + "/" + filename)
        shutil.move(cur_path,dest_path)