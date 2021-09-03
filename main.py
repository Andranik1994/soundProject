import json

import PySimpleGUI as sg
import pygame
import os.path


def play(music_file_path):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(music_file_path)
    pygame.mixer.music.play()


def stop():
    pygame.mixer.music.stop()


def pause():
    pygame.mixer.music.pause()


def unpause():
    pygame.mixer.music.unpause()


def result(data):
    scrollable_view = []
    for key, value in data.items():
        line = [
            sg.Text(key), sg.Text(value)
        ]
        scrollable_view.append(line)
        scrollable_view.append([sg.HSeparator()])
    white_spaces_for_scrollable_view1 = [sg.Text("")]
    white_spaces_for_scrollable_view2 = [sg.Text("")]
    white_spaces_for_scrollable_view3 = [sg.Text("")]
    scrollable_view.append(white_spaces_for_scrollable_view1)
    scrollable_view.append(white_spaces_for_scrollable_view2)
    scrollable_view.append(white_spaces_for_scrollable_view3)
    layout = [
        [
            sg.VSeperator(),
            sg.Column(scrollable_view, scrollable=True)
        ],
        [sg.Button(button_text="EXPORT JSON", button_color="blue", key="-EXPORT-")]
    ]

    window = sg.Window("Result", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-EXPORT-":
            with open("result.json", "w") as outfile:
                json.dump(data, outfile)
            saved = True
            window.close()
    window.close()


def main():
    # First column for choosing directory and show list of sound files
    file_list_column = [
        [
            sg.Text("File Path"),
            sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
            sg.FolderBrowse(),
        ],
        [
            sg.Listbox(values=[], enable_events=True, size=(40, 20), key="-FILE LIST-")
        ],
    ]

    # Second column for play chosen file and perform operations
    image_viewer_column = [
        [sg.Text("Sound:"), sg.Text(size=(40, 1), key="-TOUT-")],
        [sg.Text("Value:"), sg.Text(size=(40, 1), key="-TVOUT-")],
        [
            sg.Button(button_text="CLEAN", button_color="green", key="-CLEAN-", disabled=True),
            sg.Button(button_text="NOISY", button_color="red", key="-NOISY-", disabled=True)
        ],
        [sg.Button(button_text="Result", button_color="gray", key="-OBSERVE-", disabled=True)]
    ]

    layout = [
        [
            sg.Column(file_list_column),
            sg.VSeperator(),
            sg.Column(image_viewer_column)
        ]
    ]

    window = sg.Window("Andranik Sound Checker", layout)
    filename = ""
    data = {}
    is_buttons_disabled = True
    # Event Loop
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        # Folder name was filled in, make a list of files in the folder
        if event == "-FOLDER-":
            folder = values["-FOLDER-"]
            try:
                file_list = os.listdir(folder)
            except:
                file_list = []

            fnames = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(".mp3")
            ]
            window["-FILE LIST-"].update(fnames)
        elif event == "-FILE LIST-":
            try:
                if is_buttons_disabled:
                    window["-CLEAN-"].update(disabled=False)
                    window["-NOISY-"].update(disabled=False)
                    window["-OBSERVE-"].update(disabled=False)
                    is_buttons_disabled = False
                file_path = f'{values["-FOLDER-"]}/{values["-FILE LIST-"][0]}'
                filename = os.path.join(values["-FILE LIST-"][0])
                window["-TOUT-"].update(f'{filename}')
                if not filename in data:
                    window["-TVOUT-"].update("Not Checked")
                elif data[filename] == "Noisy":
                    window["-TVOUT-"].update("Noisy")
                else:
                    window["-TVOUT-"].update("Clean")
                play(file_path)
            except:
                pass
        elif event == "-CLEAN-" or event == "-NOISY-":
            value = ""
            if event == "-NOISY-":
                value = "Noisy"
            else:
                value = "Clean"
            data[filename] = value
            window["-TVOUT-"].update(f"{value}")
        elif event == "-OBSERVE-":
            pause()
            result(data)
    window.close()


if __name__ == "__main__":
    main()
