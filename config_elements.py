import PySimpleGUI as sg
import obs
from theme import *
import threading
import json


class ElementsConfig():

    def __init__(self) -> None:
        T_scn = [[sg.Text("Select Scene")]]
        S_scn = [[sg.Combo(obs.Obs().get_scenes(), default_value='Select Scene',
                        key='-SCENE-', auto_size_text=True, enable_events=True, expand_x=True, expand_y=True,readonly = True)]]
        T_elm1 = [[sg.Text("Home Serve", expand_x=True, expand_y=True)]]
        S_elm1 = [[sg.Combo([], default_value='Select Element', key='-Elm1-',
                            auto_size_text=True, enable_events=True, disabled=True, expand_x=True, expand_y=True,readonly = True)]]
        T_elm2 = [[sg.Text("Away Serve", expand_x=True, expand_y=True)]]
        S_elm2 = [[sg.Combo([], default_value='Select Element', key='-Elm2-',
                            auto_size_text=True, enable_events=True, disabled=True, expand_x=True, expand_y=True,readonly = True)]]
        T_elm3 = [[sg.Text("Home Substitution", expand_x=True, expand_y=True)]]
        S_elm3 = [[sg.Combo([], default_value='Select Element', key='-Elm3-',
                            auto_size_text=True, enable_events=True, disabled=True, expand_x=True, expand_y=True,readonly = True)]]
        T_elm4 = [[sg.Text("Away Substitution", expand_x=True, expand_y=True)]]
        S_elm4 = [[sg.Combo([], default_value='Select Element', key='-Elm4-',
                            auto_size_text=True, enable_events=True, disabled=True, expand_x=True, expand_y=True,readonly = True)]]
        T_elm5 = [[sg.Text("Time Out", expand_x=True, expand_y=True)]]
        S_elm5 = [[sg.Combo([], default_value='Select Element', key='-Elm5-',
                            auto_size_text=True, enable_events=True, disabled=True, expand_x=True, expand_y=True,readonly = True)]]
        T_elm6 = [[sg.Text("Match Point", expand_x=True, expand_y=True)]]
        S_elm6 = [[sg.Combo([], default_value='Select Element', key='-Elm6-',
                            auto_size_text=True, enable_events=True, disabled=True, expand_x=True, expand_y=True,readonly = True)]]
        T_elm7 = [[sg.Text("Set Point", expand_x=True, expand_y=True)]]
        S_elm7 = [[sg.Combo([], default_value='Select Element', key='-Elm7-',
                            auto_size_text=True, enable_events=True, disabled=True, expand_x=True, expand_y=True,readonly = True)]]
        T_elm8 = [[sg.Text("Home Points", expand_x=True, expand_y=True)]]
        S_elm8 = [[sg.Combo([], default_value='Select Element', key='-Elm8-',
                            auto_size_text=True, enable_events=True, disabled=True, expand_x=True, expand_y=True,readonly = True)]]
        T_elm9 = [[sg.Text("Away Points", expand_x=True, expand_y=True)]]
        S_elm9 = [[sg.Combo([], default_value='Select Element', key='-Elm9-',
                            auto_size_text=True, enable_events=True, disabled=True, expand_x=True, expand_y=True,readonly = True)]]
        T_elm10 = [[sg.Text("Home Name", expand_x=True, expand_y=True)]]
        S_elm10 = [[sg.Combo([], default_value='Select Element', key='-Elm10-',
                            auto_size_text=True, enable_events=True, disabled=True, expand_x=True, expand_y=True,readonly = True)]]
        T_elm11 = [[sg.Text("Away Name", expand_x=True, expand_y=True)]]
        S_elm11 = [[sg.Combo([], default_value='Select Element', key='-Elm11-',
                            auto_size_text=True, enable_events=True, disabled=True, expand_x=True, expand_y=True,readonly = True)]]
        T_elm12 = [[sg.Text("Home Sets", expand_x=True, expand_y=True)]]
        S_elm12 = [[sg.Combo([], default_value='Select Element', key='-Elm12-',
                            auto_size_text=True, enable_events=True, disabled=True, expand_x=True, expand_y=True,readonly = True)]]
        T_elm13 = [[sg.Text("Away Sets", expand_x=True, expand_y=True)]]
        S_elm13 = [[sg.Combo([], default_value='Select Element', key='-Elm13-',
                            auto_size_text=True, enable_events=True, disabled=True, expand_x=True, expand_y=True,readonly = True)]]
        T_Save = [[sg.Text("Saved", key="-SAVE_TXT-", visible=False)]]
        B_Save = [[sg.Button("Save", key="-SAVE-")]]
        layout = [
            [sg.Column(T_scn, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(S_scn, element_justification='left', expand_x=True, expand_y=True)],
            [sg.HorizontalSeparator(pad=(10,10))],
            [sg.Column(T_elm10, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(S_elm10, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(T_elm11, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(S_elm11, element_justification='left', expand_x=True, expand_y=True)],
            [sg.Column(T_elm1, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(S_elm1, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(T_elm2, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(S_elm2, element_justification='left', expand_x=True, expand_y=True)],
            [sg.Column(T_elm3, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(S_elm3, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(T_elm4, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(S_elm4, element_justification='left', expand_x=True, expand_y=True)],
            [sg.Column(T_elm8, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(S_elm8, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(T_elm9, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(S_elm9, element_justification='left', expand_x=True, expand_y=True)],
            [sg.Column(T_elm12, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(S_elm12, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(T_elm13, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(S_elm13, element_justification='left', expand_x=True, expand_y=True)],
            [sg.Column(T_elm5, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(S_elm5, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(T_elm6, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(S_elm6, element_justification='left', expand_x=True, expand_y=True)],
            [sg.Column(T_elm7, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(S_elm7, element_justification='left', expand_x=True, expand_y=True)],
            [sg.Column(B_Save, element_justification='left', expand_x=True, expand_y=True),
            sg.Column(T_Save, element_justification='left', expand_x=True, expand_y=True)]
        ]
        self.window = sg.Window("LivoStream - Config", icon=logo,
                        layout=layout, font=("Bebas", 15), auto_size_text=True, auto_size_buttons=True, modal=True, resizable=True, finalize=True, size=(800,400))
        width, height = sg.Window.get_screen_size()
        # try:
        #     self.get_config()
        # except Exception as e:
        #     print(e)
        #     sg.Popup('Configurar', keep_on_top=True)
        self.get_config()
        while True:
            event, values = self.window.read()
            print(event, values)
            if event == '-SCENE-':
                self.get_elements(values['-SCENE-'])
            elif event == '-SAVE-':
                self.save_config()
            elif event == "Exit" or event == sg.WIN_CLOSED:
                break

        self.window.close()

    def get_config(self):
        with open('elem_config.json', 'r') as openfile:
            # Reading from json file
            config = json.load(openfile)
            items = self.get_elements(config['SCENE'])
            x = 1
            if items != "ERROR":
                for key in config:
                    if key == "SCENE":
                        self.window['-SCENE-'].update(value=config[key],
                                                    visible=True)
                    else:
                        #self.window['-Elm'+str(x)+'-'].update(value=list(items.keys())[list(items.values()).index(config[key])], visible=True, disabled=False)
                        if type(config[key]) == str:
                            self.window['-Elm'+str(x)+'-'].update(value=config[key], visible=True, disabled=False)
                        else:
                            self.window['-Elm'+str(x)+'-'].update(value=[name for name, element in items.items() if element.get('id') == config[key]][0], visible=True, disabled=False)
                        x = x+1

    def get_elements(self,scene):
        items = obs.Obs().get_scene_items(scene)
        if items != "ERROR":
            elements = []
            for x in items:
                elements.append(x)
            for x in range(1, 14):
                self.window['-Elm'+str(x)+'-'].update(values=elements,
                                                 visible=True, disabled=False)
        return items

    def save_config(self):
        event, values = self.window.read()
        elements = obs.Obs().get_scene_items(values['-SCENE-'])
        if elements != "ERROR":
            # Data to be written
            dictionary = {
                "SCENE": values['-SCENE-'],
                "H_SERVE": elements[values['-Elm1-']]['id'],
                "A_SERVE": elements[values['-Elm2-']]['id'],
                "H_SUBSTITUTION": elements[values['-Elm3-']]['id'],
                "A_SUBSTITUTION": elements[values['-Elm4-']]['id'],
                "TIME_OUT": elements[values['-Elm5-']]['id'],
                "MATCH_POINT": elements[values['-Elm6-']]['id'],
                "SET_POINT": elements[values['-Elm7-']]['id'],
                "HOME_POINTS": elements[values['-Elm8-']]['name'],
                "AWAY_POINTS": elements[values['-Elm9-']]['name'],
                "HOME_NAME": elements[values['-Elm10-']]['name'],
                "AWAY_NAME": elements[values['-Elm11-']]['name'],
                "HOME_SET": elements[values['-Elm12-']]['name'],
                "AWAY_SET": elements[values['-Elm13-']]['name'],
            }

            # Serializing json
            json_object = json.dumps(dictionary, indent=4)
            with open("elem_config.json", "w") as outfile:
                outfile.write(json_object)
                self.window['-SAVE_TXT-'].update(visible=True)
                                  
                                  