import PySimpleGUI as sg
import os
from chroma import import_foreground, import_background, set_thres, set_channel, cutout_show, export
from audio import setup_mixer, set_pitch, set_speed, play_audio, stop_audio, export_audio, load_audio, cleanup_audio, set_limit

working_directory = os.getcwd()

valid_audio = False
valid_start = True
valid_end = True

def update_img_preview():
    bytes = cutout_show()
    if bytes != None:
        window['preview_image'].update(data=bytes)
        window['EXPORT'].update(disabled=False)

def enable_play():
    global valid_audio, valid_start, valid_end
    isvalid = valid_audio and valid_start and valid_end
    window["MUSIC_PLAY"].update(disabled=not isvalid)
    window["MUSIC_EXPORT"].update(disabled=not isvalid)

def cuts_info(end, msg):
    global valid_start
    global valid_end
    if end:
        valid_end = msg == ""
        window['CROP_END_WARN'].update(msg)
    else:
        valid_start = msg == ""
        window['CROP_START_WARN'].update(msg)
    enable_play()
    

def calc_seconds(str, end):
    format_msg = "Invalid format: Must be hh:mm:ss, mm:ss, ss"
    if str == "":
        set_limit(-1, end)
        cuts_info(end, "")
        return
    str = str.split(":")
    if len(str) > 3:
        cuts_info(end, format_msg)
        return
    str = str[::-1]
    acc = 1
    secs = 0
    for elem in str:
        try:
            elem = int(elem)
        except ValueError:
            cuts_info(end, format_msg)
            return
        if (acc != 3600 and elem > 60) or elem < 0:
            cuts_info(end, format_msg)
            return
        secs += elem*acc
        acc *= 60
    message = set_limit(secs, end)
    cuts_info(end, message)


def background_layout():
    return  [[sg.Text("Choose a background file:")],
            [sg.InputText(key="-FILE_PATH_BG-"), 
            sg.FileBrowse(initial_folder=working_directory, file_types=[("JPG Files", "*.jpg")]),
            sg.Button('OK', key="Submit_BG")
            ]]

def chroma_options_layout():
    return [[
        sg.Column([
        [sg.Text("Channel")],
        [sg.Radio('R', "RADIOCHANNEL", key="RADIOCHANNEL", default=True, enable_events=True)],
        [sg.Radio('G', "RADIOCHANNEL", key="RADIOCHANNEL", default=False, enable_events=True)],
        [sg.Radio('B', "RADIOCHANNEL", key="RADIOCHANNEL", default=False, enable_events=True)],
    ])
]]

tab1 = [[  sg.Column(
            [[sg.Text("Choose a foreground file:")],
            [sg.InputText(key="-FILE_PATH_FG-", enable_events=True), 
            sg.FileBrowse(initial_folder=working_directory, file_types=[("JPG Files", "*.jpg")])
            ],
            [sg.Text("Choose a background file:")],
            [sg.InputText(key="-FILE_PATH_BG-", enable_events=True), 
            sg.FileBrowse(initial_folder=working_directory, file_types=[("JPG Files", "*.jpg")])
            ],
            [sg.Column([
            [sg.Text("Channel")],
            [sg.Radio('R', "RADIOCHANNEL", key="RADIOCHANNEL", default=True, enable_events=True)],
            [sg.Radio('G', "RADIOCHANNEL", key="RADIOCHANNEL", default=False, enable_events=True)],
            [sg.Radio('B', "RADIOCHANNEL", key="RADIOCHANNEL", default=False, enable_events=True)],
            ]),
            sg.Column([[sg.Text("Threshold")],[sg.Slider((0,256), 128, 1, orientation='horizontal', key="THR_SLIDER", enable_events = True)]], vertical_alignment='t'),
            sg.InputText(key="IMAGE_SAVE", do_not_clear=False, visible=False, enable_events=True), 
            sg.FileSaveAs("Export",initial_folder=working_directory, file_types=[("JPG Files", "*.jpg")], key = "EXPORT", enable_events = True, disabled=True)
            ],
            ],
            key="CHROMA"),
            sg.Image(key='preview_image',size=(600,450)),
        ]]

tab2 = [
    [sg.Text("Choose a file: ", size=(12,1)), sg.Input(key="MUSIC_PATH", enable_events=True),
     sg.FileBrowse(initial_folder=working_directory, file_types=[("Audio Files", "*.mp3 *.wav")])],
    [sg.Text("Start: ", size=(12, 1)), sg.Input(key="MUSIC_CROP_START", enable_events=True),
     sg.Text("", key='CROP_START_WARN')],
    [sg.Text("End: ", size=(12, 1)), sg.Input(key="MUSIC_CROP_END", enable_events=True),
     sg.Text("", key='CROP_END_WARN')],
    [
    sg.vbottom(sg.Text("Speed")),
    sg.Slider((0.05,2), 1, 0.025, orientation='horizontal', key="SPEED_SLIDER", enable_events = True),
    sg.vbottom(sg.Checkbox("Keep pitch", False, key="PITCH_BOX", enable_events=True))
    ],
    [sg.Text("Length (loops): ", size=(12, 1)), sg.Input()],
    [sg.Text(size=(12,1), key='MUSIC_STATUS')],
    [
        sg.Button('Play', pad=(10, 0), key='MUSIC_PLAY', disabled=True),
        sg.Button('Pause', pad=(10, 0), key='MUSIC_PAUSE',disabled=True),
        sg.InputText(key="MUSIC_SAVE", do_not_clear=False, visible=False, enable_events=True),
        sg.FileSaveAs("Export",initial_folder=working_directory, file_types=[("WAV", "*.wav")], key = "MUSIC_EXPORT", enable_events = True, disabled=True)
    ]
]

layout = [[sg.TabGroup([
   [sg.Tab('Chroma Key', tab1),
   sg.Tab('Audio Edit', tab2)]])],
]

window = sg.Window("Multimedia App", layout)

setup_mixer()

try:
    while True:
        event, values = window.read()

        print(event)



        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == "-FILE_PATH_FG-":
            fg_address = values["-FILE_PATH_FG-"]
            import_foreground(fg_address)
            update_img_preview()
            #window.extend_layout(window['CHROMA'], background_layout())
        elif event == "-FILE_PATH_BG-":
            bg_address = values["-FILE_PATH_BG-"]
            import_background(bg_address)
            update_img_preview()
            #window.extend_layout(window['CHROMA'], chroma_options_layout())
        elif event == "RADIOCHANNEL":
            set_channel(0)
            update_img_preview()
        elif event == "RADIOCHANNEL1":
            set_channel(1)
            update_img_preview()
        elif event == "RADIOCHANNEL2":
            set_channel(2)
            update_img_preview()
        elif event == "THR_SLIDER":
            set_thres(values["THR_SLIDER"])
            update_img_preview()
        elif event == "IMAGE_SAVE":
            export(values["IMAGE_SAVE"])
        elif event == "MUSIC_PATH":
            valid_audio = load_audio(values["MUSIC_PATH"])
            calc_seconds(values["MUSIC_CROP_START"], False)
            calc_seconds(values["MUSIC_CROP_END"], True)
        elif event == "PITCH_BOX":
            set_pitch(values["PITCH_BOX"])
        elif event == "SPEED_SLIDER":
            set_speed(values["SPEED_SLIDER"])
        elif event == "MUSIC_PLAY":
            play_audio()
            window["MUSIC_PAUSE"].update(disabled=False)
            window['MUSIC_STATUS'].update('Playing')
        elif event == "MUSIC_PAUSE":
            if stop_audio():
                window['MUSIC_STATUS'].update('Playing')
            else:
                window['MUSIC_STATUS'].update('Paused')
        elif event == "MUSIC_SAVE":
            export_audio(values["MUSIC_SAVE"])
        elif event == "MUSIC_CROP_START":
            calc_seconds(values["MUSIC_CROP_START"], False)
        elif event == "MUSIC_CROP_END":
            calc_seconds(values["MUSIC_CROP_END"], True)
except Exception as exception:
    print(type(exception).__name__)
    cleanup_audio()

window.close()
cleanup_audio()