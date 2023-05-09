from pygame import mixer, time
import pygame
import librosa
import os
import soundfile as sf
import datetime
import numpy as np



sound_series = []
sr = 0

transition_length = 0
seconds = 0

def load_vid_audio(path):
    global sound_series
    global sr
    global seconds
    try:
        sound_series, sr = librosa.load(path)
        seconds = librosa.get_duration(y=sound_series, sr=sr)
    except:
        return False

    return True

def get_len():
    return seconds

def set_transition_length(val):
    global transition_length
    transition_length = val