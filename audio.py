from pygame import mixer, time
import pygame
import librosa
import os
import soundfile as sf


speed = 1.0
pitch_kept = False
updated = False
is_playing = False
mix_sound = 0
sound_series = []
sr = 0
start_crop = -1
end_crop = -1
max_seconds = 0

def set_limit(seconds, isend):
    global start_crop
    global end_crop
    global updated
    global max_seconds
    #print(seconds)
    #print(max_seconds)
    if seconds != -1 and seconds > max_seconds:
        return "Must be less than music length"
    if isend:
        if seconds != -1 and seconds <= start_crop:
            return "Must be more than start"
        end_crop = seconds
    else:
        start_crop = seconds
    updated = False
    return ""


def setup_mixer():
    mixer.init()

def set_pitch(val):
    global updated
    global pitch_kept
    pitch_kept = val
    updated = False

def set_speed(val):
    global speed
    global updated
    speed = val
    updated = False

def load_audio(path):
    global sound_series
    global sr
    global updated
    global max_seconds
    try:
        sound_series, sr = librosa.load(path)
        max_seconds = librosa.get_duration(y=sound_series, sr=sr)
        updated = False
    except:
        return False

    #print(sound_series)
    return True

def crop_audio(series, sr):
    #print(start_crop)
    #print(end_crop)
    cut_at_start = 0
    if start_crop != -1:
        cut_at_start = sr * start_crop
    cut_at_end = len(series)
    if end_crop != -1:
        cut_at_end = sr*end_crop
    #print(cut_at_start)
    #print(cut_at_end)
    #print(len(series))

    return series[cut_at_start : cut_at_end]


    

def update_audio():
    global sound_series

    mod_series = sound_series
    mod_sr = sr

    mod_series = crop_audio(mod_series, mod_sr)
    
    if pitch_kept:
        mod_series = librosa.effects.time_stretch(mod_series, rate=speed)
    else:
        mod_sr = int(sr*speed)

    return mod_series, mod_sr


def play_audio():
    global is_playing
    global updated



    if not updated:
        mod_series, mod_sr = update_audio()
        unload()
        sf.write('temp.wav', mod_series, mod_sr, 'PCM_24')
        pygame.mixer.music.load('temp.wav')
        updated = True
    
    mixer.music.play()
    is_playing = True

def stop_audio():
    global is_playing
    if is_playing:
        mixer.music.pause()
        is_playing = False
    else:
        mixer.music.unpause()
        is_playing = True
    return is_playing

def export_audio(path):
    mod_series, mod_sr = update_audio()
    sf.write(path, mod_series, mod_sr, 'PCM_24')

def unload():
    mixer.music.unload()

def cleanup_audio():
    unload()
    try:
        os.remove("temp.wav")
    except:
        return
