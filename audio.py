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
    try:
        sound_series, sr = librosa.load(path)
    except:
        return True

    #print(sound_series)
    return False
    

def update_audio():
    global sound_series

    mod_series = sound_series
    mod_sr = sr
    
    if pitch_kept:
        mod_series = librosa.effects.time_stretch(sound_series, rate=speed)
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
    os.remove("temp.wav")
