import PySimpleGUI as sg
import os
from chroma import import_foreground, import_background, set_thres, set_channel, cutout_show

working_directory = os.getcwd()

def update_img_preview():
    bytes = cutout_show()
    if bytes != None:
        window['preview_image'].update(data=bytes)

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
            sg.FileSaveAs(initial_folder=working_directory, file_types=[("JPG Files", "*.jpg")], key = "EXPORT", enable_events = True)
            ],
            [sg.Image(key='preview_image',size=(450,250))],
            ],
            key="CHROMA"),
        ]]

window = sg.Window("Multimedia App", layout)

while True:
    event, values = window.read(timeout=20)
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

window.close()
