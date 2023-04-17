import PySimpleGUI as sg
import os
from chroma import import_foreground, import_background, set_thres, set_channel, cutout_show, export
from pygame import mixer, time
import pygame

working_directory = os.getcwd()

def update_img_preview():
    bytes = cutout_show()
    if bytes != None:
        window['preview_image'].update(data=bytes)
        window['EXPORT'].update(disabled=False)

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
    [sg.Text("Choose a file: ", size=(12,1)), sg.Input(), sg.FileBrowse(key="MUSIC_PATH")],
    [sg.Text("Start: ", size=(12, 1)), sg.Input()],
    [sg.Text("End: ", size=(12, 1)), sg.Input()],
    [
    sg.vbottom(sg.Text("Speed")),
    sg.Slider((0.1,5), 1, 0.1, orientation='horizontal', key="SPEED_SLIDER", enable_events = True),
    sg.vbottom(sg.Checkbox("Keep pitch", False))
    ],
    [sg.Text("Length (loops): ", size=(12, 1)), sg.Input()],
    [sg.Text(size=(12,1), key='MUSIC_STATUS')],
    [
        sg.Button('Play', pad=(10, 0), key='MUSIC_PLAY', disabled=True),
        sg.Button('Stop', pad=(10, 0), key='MUSIC_STOP',disabled=True),
        sg.Button('Export', pad=(10, 0), key='MUSIC_EXPORT',disabled=True)
    ]
]

layout = [[sg.TabGroup([
   [sg.Tab('Chroma Key', tab1),
   sg.Tab('Audio Edit', tab2)]])],
]

window = sg.Window("Multimedia App", layout)

mixer.init()
is_playing = False

current_position = 0

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

window.close()
