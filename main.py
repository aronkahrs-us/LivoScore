import PySimpleGUI as sg
import threading
import json
from theme import *
from config_elements import ElementsConfig
from config_obs import ObsConfig
from config_league import LeagueConfig
from Utils.obs import Obs
from Utils.apiv3 import Match
from Utils.league import League
from Utils.court import Court

class Main:
    def __init__(self) -> None:
        DISPLAY_TIME_MILLISECONDS = 1000

        # All the stuff inside your self.window.
        T_Local = [[sg.Text("Local", auto_size_text=True, key='-HOME-',
                        visible=False, expand_x=True, expand_y=True, justification='center')]]
        T_Visita = [[sg.Text("Visita", auto_size_text=True,
                        key='-AWAY-', visible=False, expand_x=True, expand_y=True, justification='center')]]
        B_Iniciar = [[sg.Button("Iniciar", key="-ST-", border_width=0, disabled=True)]]
        B_Reload= [[sg.Button("🔄", key="-RELOAD-", button_color="#002B45")]]
        T_Error = [[sg.Text("", auto_size_text=True,
                            key='-ERROR-', visible=True, text_color="red", expand_x=True, expand_y=True, size=30, justification='center')]]
        T_Id = [
            [sg.Text("Id de partido", text_color="white", justification="center")]]
        I_Id = [[sg.Combo([], default_value='Cargando...', key='-ID-',
                            auto_size_text=True, enable_events=True, disabled=True, expand_x=True, expand_y=True, size=(30,10),readonly = True)]]
        layout = [
            [sg.Menu(menu_def, font=('Bebas', 15))],
            [sg.Text("Livoscore", expand_x=True,
                    text_color="#ffffff", click_submits=True, justification='center', font=('Bebas', 25))],
            [sg.Column(T_Id, element_justification='c', expand_x=True, expand_y=True),
            sg.Column(I_Id, element_justification='c', expand_x=True, expand_y=True),
            sg.Column(B_Reload, element_justification='c', expand_x=True, expand_y=True)],
            [sg.Column(B_Iniciar, element_justification='c', expand_x=True, expand_y=True),
            sg.Column(T_Error, element_justification='center', expand_x=True, expand_y=True)],
            [sg.Column(T_Local, element_justification='c', expand_x=True, expand_y=True),
            sg.Column(T_Visita, element_justification='c', expand_x=True, expand_y=True)]
        ]
        # Create the Window
        # splash = sg.Window("Livoscore", icon=logo,
        #                 layout=[[sg.Image(data=logo)]], transparent_color="#002b45", no_titlebar=True, keep_on_top=True).read(timeout=DISPLAY_TIME_MILLISECONDS, close=True)
        self.window = sg.Window("Livoscore", icon=logo,
                        layout=layout, font=("Bebas", 15), auto_size_text=True, resizable=True, auto_size_buttons=True, finalize=True)
        threading.Thread(target=self.list_matches, daemon=True).start()
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, self.values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes self.window or clicks cancel
                self.match._stop()
                break
            elif event == 'Obs Elements':  # if user closes self.window or clicks cancel
                if Obs().test_connection() != 'ERROR':
                    ElementsConfig()
                else:
                    self.window['-ERROR-'].update("Falta configurar OBS o está cerrado", text_color='red', visible=True)
            elif event == 'Obs Config':  # if user closes self.window or clicks cancel
                ObsConfig()
            elif event == 'API Config':  # if user closes self.window or clicks cancel
                LeagueConfig()
            elif event == '-ID-' and self.values['-ID-'] != '':  # if user closes self.window or clicks cancel
                self.window['-ST-'].update(disabled=False)
            elif event == '-ST-':
                try:
                    if self.match.is_running:
                        self.match._stop()
                    else:
                        threading.Thread(target=self.start_match, daemon=True).start()
                except:
                    threading.Thread(target=self.start_match, daemon=True).start()
            elif event == '-RELOAD-':
                threading.Thread(target=self.list_matches, daemon=True).start()

        self.window.close()
    def list_matches(self):
        try:
            with open('./Config/api_config.json', 'r') as openfile:
                # Reading from json file
                config = json.load(openfile)
            self.window['-ID-'].update(values=[],value='Cargando...', visible=True, disabled=True)
            self.window['-RELOAD-'].update(disabled=True)
            self.matches = League().get_ready_matches()
            if self.matches == {}:
                self.window['-ID-'].update(values=[],value='No hay partidos', visible=True, disabled=True)
            else:
                self.window['-ID-'].update(values=[self.matches[x] for x in self.matches],value='Selecionar partido', visible=True, disabled=False)
            self.window['-RELOAD-'].update(disabled=False)
        except Exception as e:
            while 'window' not in locals()['self'].__dict__:
                pass
            else:
                print('OK')
                self.window['-ERROR-'].update(value='Falta configurar', visible=True)

    def start_match(self):
        if Obs().test_connection() == "ERROR":
            self.window['-ERROR-'].update("Falta configurar OBS o está cerrado", text_color='red', visible=True)
        else:
            self.window['-ERROR-'].update("Iniciando", text_color='green', visible=True)
            self.match=Match(list(self.matches.keys())[list(self.matches.values()).index(self.values['-ID-'])],self.window)
            threading.Thread(target=Court.start,args=self.match).start()