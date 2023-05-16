from pygame import mixer, time
import pygame
import librosa
import os
import soundfile as sf
import datetime
import numpy as np
import math
import cv2
import moviepy.video.io.ImageSequenceClip
from moviepy.editor import *
import threading


sound_series = []
sr = 0
audio_path = ""

transition_length = 0
clip_length = 0
seconds = 0

hor = 1280
ver = 720

def load_vid_audio(path):
    global sound_series
    global sr
    global seconds
    global audio_path
    try:
        sound_series, sr = librosa.load(path)
        seconds = librosa.get_duration(y=sound_series, sr=sr)
        audio_path = path
    except:
        return False

    return True

def get_len():
    return seconds

def set_transition_length(val):
    global transition_length
    transition_length = val

def set_clip_length(val):
    global clip_length
    clip_length = val

def set_res(str):
    global hor
    global ver
    arr = str.split('x')
    hor = int(arr[0])
    ver = int(arr[1])


def resize_image(img, size=(28,28)): #https://stackoverflow.com/a/49208362

    h, w = img.shape[:2]
    c = img.shape[2] if len(img.shape)>2 else 1

    if h == w: 
        return cv2.resize(img, size, cv2.INTER_AREA)

    dif = h if h > w else w

    interpolation = cv2.INTER_AREA if dif > (size[0]+size[1])//2 else cv2.INTER_CUBIC

    x_pos = (dif - w)//2
    y_pos = (dif - h)//2

    if len(img.shape) == 2:
        mask = np.zeros((dif, dif), dtype=img.dtype)
        mask[y_pos:y_pos+h, x_pos:x_pos+w] = img[:h, :w]
    else:
        mask = np.zeros((dif, dif, c), dtype=img.dtype)
        mask[y_pos:y_pos+h, x_pos:x_pos+w, :] = img[:h, :w, :]

    return cv2.resize(mask, size, interpolation)

def create_video(images, path, logger):

    thr = threading.Thread(target=thr_vid, args=(images, path, logger), kwargs={})
    thr.start()

def thr_vid(images, path, logger):
    image_frames = math.floor(clip_length * 30) 
    transition_frames = math.floor(transition_length*30)
    print(image_frames)
    print(transition_frames)
    #full_frames = image_frames-transition_length

    img_arrays = map(lambda x: cv2.cvtColor(resize_image(cv2.imread(x), (hor, ver)), cv2.COLOR_BGR2RGB), images)
    video_array = []

    last_img = np.zeros((ver, hor, 3), dtype = np.uint8)
    for img in img_arrays:
        frame = 0
        while frame < image_frames:
            new_img = img
            if frame < transition_frames:
                weight = frame / transition_frames
                new_img = cv2.addWeighted(last_img, 1-weight, img, weight, 0)
            video_array.append(new_img)
            frame += 1
        last_img = img

    #print(video_array)

    clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(video_array, fps=30)
    audioclip = AudioFileClip(audio_path)

    new_audioclip = CompositeAudioClip([audioclip])
    clip.audio = new_audioclip
    clip.write_videofile(path, logger=logger)