import PySimpleGUI as sg
import os
from chroma import import_foreground, import_background, set_thres, set_channel, cutout_show

working_directory = os.getcwd()

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

layout = [[  sg.Column(
            [[sg.Text("Choose a foreground file:")],
            [sg.InputText(key="-FILE_PATH_FG-"), 
            sg.FileBrowse(initial_folder=working_directory, file_types=[("JPG Files", "*.jpg")]),
            sg.Button('OK', key="Submit_FG")
            ],
            [sg.Text("Choose a background file:")],
            [sg.InputText(key="-FILE_PATH_BG-"), 
            sg.FileBrowse(initial_folder=working_directory, file_types=[("JPG Files", "*.jpg")]),
            sg.Button('OK', key="Submit_BG")
            ],
            [sg.Column([
            [sg.Text("Channel")],
            [sg.Radio('R', "RADIOCHANNEL", key="RADIOCHANNEL", default=True, enable_events=True)],
            [sg.Radio('G', "RADIOCHANNEL", key="RADIOCHANNEL", default=False, enable_events=True)],
            [sg.Radio('B', "RADIOCHANNEL", key="RADIOCHANNEL", default=False, enable_events=True)],
            ]),
            sg.Column([[sg.Text("Threshold")],[sg.Slider((0,256), 128, 1, orientation='horizontal', key="THR_SLIDER")]], vertical_alignment='t'),
            sg.Column([[sg.Button('Pre-visualize', key="PREVIS")]], vertical_alignment='t')
            ]], key="CHROMA")
        ]]

window = sg.Window("Multimedia App", layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == "Submit_FG":
        fg_address = values["-FILE_PATH_FG-"]
        import_foreground(fg_address)
        #window.extend_layout(window['CHROMA'], background_layout())
    elif event == "Submit_BG":
        bg_address = values["-FILE_PATH_BG-"]
        import_background(bg_address)
        #window.extend_layout(window['CHROMA'], chroma_options_layout())
    elif event == "RADIOCHANNEL":
        set_channel(0)
    elif event == "RADIOCHANNEL0":
        set_channel(1)
    elif event == "RADIOCHANNEL1":
        set_channel(2)
    elif event == "THR_SLIDER":
        set_thres(values["THR_SLIDER"])
    elif event == "PREVIS":
        cutout_show()

window.close()
