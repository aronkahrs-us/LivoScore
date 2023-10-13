import PySimpleGUI as sg
import obs
from theme import *
import threading
import json

class ObsConfig():
    def __init__(self) -> None:
        T_ip = [[sg.Text("Ip Address")]]
        S_ip = [[sg.Input('', enable_events=True,  key='-IP-')]]
        T_port = [[sg.Text("Port")]]
        S_port= [[sg.Input('', enable_events=True,  key='-PORT-')]]
        T_pass = [[sg.Text("Password")]]
        S_pass= [[sg.Input('', enable_events=True,  key='-PASS-')]]
        T_Save = [[sg.Text("Saved", key="-SAVE_TXT-", visible=False)]]
        B_Save= [[sg.Button("Save", key="-SAVE-")]]
        B_Test= [[sg.Button("Test Connection", key="-TEST-")]]
        layout = [
                    [sg.Column(T_ip, element_justification='c', expand_x=True, expand_y=True),sg.Column(S_ip, element_justification='c', expand_x=True, expand_y=True)],
                    [sg.Column(T_port, element_justification='c', expand_x=True, expand_y=True),sg.Column(S_port, element_justification='c', expand_x=True, expand_y=True)],
                    [sg.Column(T_pass, element_justification='c', expand_x=True, expand_y=True),sg.Column(S_pass, element_justification='c', expand_x=True, expand_y=True)],
                    [sg.Column(B_Save, element_justification='c', expand_x=True, expand_y=True),sg.Column(B_Test, element_justification='c', expand_x=True, expand_y=True),sg.Column(T_Save, element_justification='c', expand_x=True, expand_y=True)],
                ]
        self.window = sg.Window("LivoStream - OBS Config", icon=logo,
                        layout=layout, font=("Bebas", 15), auto_size_text = True, auto_size_buttons = True, modal= True,resizable=True, finalize=True)
        try:
            self.get_config()
        except Exception as e:
            print(e)
            sg.Popup('Configurar', keep_on_top=True)

        while True:
            event, values = self.window.read()
            print(event, values)
            if event == '-SAVE-':
                self.save_config()
            elif event == '-TEST-':
                self.test_config()
            elif event == "Exit" or event == sg.WIN_CLOSED:
                break
            
        self.window.close()

    def get_config(self):
        with open('obs_config.json', 'r') as openfile:
            # Reading from json file
            config = json.load(openfile)
            self.window['-IP-'].update(value=config['IP'], visible=True)
            self.window['-PORT-'].update(value=config['PORT'], visible=True)
            self.window['-PASS-'].update(value=config['PASS'], visible=True)

    def test_config(self):
        if obs.test_connection() != "ERROR":
            self.window['-SAVE_TXT-'].update(value="OK", text_color='green', visible=True)
        else:
            self.window['-SAVE_TXT-'].update(value="ERROR", text_color='red', visible=True)

    def save_config(self):
        event, values = self.window.read()
        # Data to be written
        dictionary = {
            "IP": values['-IP-'],
            "PORT": values['-PORT-'],
            "PASS": values['-PASS-']
        }
        
        # Serializing json
        json_object = json.dumps(dictionary, indent=4)
        with open("obs_config.json", "w") as outfile:
            outfile.write(json_object)
            self.window['-SAVE_TXT-'].update('Saved', text_color='white', visible=True)