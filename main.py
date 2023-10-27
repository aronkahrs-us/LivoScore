import PySimpleGUI as sg
import threading
import json
import requests
import platform, os
from theme import *
from config_elements import ElementsConfig
from config_stream import StreamConfig
from config_league import LeagueConfig
from Utils.obs import Obs
from Utils.vmix import Vmix
from Utils.apiv3 import Match
from Utils.league import League
from Utils.court import Court
from Utils.remote import Remote


class Main:
    def __init__(self) -> None:
        try:
            with open("./Config/stream_config.json", "r") as openfile:
                # Reading from json file
                config = json.load(openfile)
                self.is_obs = config["OBS"]
                self.is_vmix = config["VMIX"]
                self.streamer = Obs() if self.is_obs else Vmix()
        except Exception as e:
            sg.popup_error(f"AN EXCEPTION OCCURRED!", e)
        sg.theme('LIVO')
        # All the stuff inside your self.window.
        T_Local = [
            [
                sg.Text(
                    "Home",
                    auto_size_text=True,
                    key="-HOME-",
                    visible=False,
                    expand_x=True,
                    expand_y=True,
                    justification="center",
                )
            ]
        ]
        T_Visita = [
            [
                sg.Text(
                    "Guest",
                    auto_size_text=True,
                    key="-AWAY-",
                    visible=False,
                    expand_x=True,
                    expand_y=True,
                    justification="center",
                )
            ]
        ]
        B_Iniciar = [[sg.Button("Start", key="-ST-", border_width=0, disabled=True)]]
        B_Reload = [[sg.Button("🔄", key="-RELOAD-", button_color="#002B45", border_width=0)]]
        T_Error = [
            [
                sg.Text(
                    "",
                    auto_size_text=True,
                    key="-ERROR-",
                    visible=True,
                    text_color="red",
                    expand_x=True,
                    expand_y=True,
                    size=30,
                    justification="c",
                )
            ]
        ]
        T_Id = [[sg.Text("Match", text_color="white", justification="center")]]
        I_Id = [
            [
                sg.Combo(
                    [],
                    default_value="Loading...",
                    key="-ID-",
                    auto_size_text=True,
                    enable_events=True,
                    disabled=True,
                    expand_x=True,
                    expand_y=True,
                    size=(30, 10),
                    readonly=True,
                )
            ]
        ]
        layout = [
            [sg.Menu(menu_def, font=("Bebas", 15))],
            [
                sg.Column(
                    T_Id, element_justification="c", expand_x=True, expand_y=True
                ),
                sg.Column(
                    I_Id, element_justification="c", expand_x=True, expand_y=True
                ),
                sg.Column(
                    B_Reload, element_justification="c", expand_x=True, expand_y=True
                ),
            ],
            [
                sg.Column(
                    B_Iniciar, element_justification="c", expand_x=True, expand_y=True
                ),
                sg.Column(
                    T_Error,
                    element_justification="center",
                    expand_x=True,
                    expand_y=True,
                ),
            ],
            [
                sg.Column(
                    T_Local, element_justification="c", expand_x=True, expand_y=True
                ),
                sg.Column(
                    T_Visita, element_justification="c", expand_x=True, expand_y=True
                ),
            ],
        ]
        # Create the Window
        # splash = sg.Window("Livoscore", icon=logo,
        #                 layout=[[sg.Image(data=logo)]], transparent_color="#002b45", no_titlebar=True, keep_on_top=True).read(timeout=DISPLAY_TIME_MILLISECONDS, close=True)
        if platform.system() == "Darwin":
            try:
                original_umask = os.umask(0)
                os.makedirs("Config", 0o777, exist_ok=True)
            except Exception as e:
                print(e)
            finally:
                os.umask(original_umask)
        else:
            os.makedirs("Config", exist_ok=True)
        self.window = sg.Window(
            "Livoscore",
            icon=logo,
            layout=layout,
            font=("Bebas Neue", 15),
            auto_size_text=True,
            resizable=True,
            auto_size_buttons=True,
            finalize=True,
            border_depth=0,
            titlebar_background_color="#002B45",
        )
        threading.Thread(target=self.list_matches, daemon=True).start()
        remt=Remote(self.window)
        threading.Thread(target=remt.run, daemon=True).start()
        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, self.values = self.window.read()
            print(event,self.values)
            try:
                print('match: ',self.match.is_running)
            except:
                pass
            if (event == sg.WIN_CLOSED or event == "Cancel"):  # if user closes self.window or clicks cancel
                if "match" in locals()["self"].__dict__:
                    self.match._stop()
                break
            elif event == "Stream Elements":  # if user closes self.window or clicks cancel
                if self.streamer.test_connection() != "ERROR":
                    ElementsConfig()
                else:
                    self.window["-ERROR-"].update(
                        "OBS not configured or closed",
                        text_color="red",
                        visible=True,
                    )
            elif event == "Stream Config":  # if user closes self.window or clicks cancel
                StreamConfig()
            elif (
                event == "League Config"
            ):  # if user closes self.window or clicks cancel
                LeagueConfig()
            elif (
                event == "-ID-" and self.values["-ID-"] != ""
            ):  # if user closes self.window or clicks cancel
                self.window["-ST-"].update(disabled=False)
            elif event == "-ST-":
                try:
                    print('try')
                    if self.match.is_running == True:
                        self.court.stop()
                        self.match._stop()
                    else:
                        print('start')
                        threading.Thread(target=self.start_match, daemon=True).start()
                except Exception as e:
                    print('excp',e)
                    threading.Thread(target=self.start_match, daemon=True).start()
            elif event == "-RELOAD-":
                threading.Thread(target=self.list_matches, daemon=True).start()

        self.window.close()

    def list_matches(self):
        try:
            with open("./Config/league_config.json", "r") as openfile:
                # Reading from json file
                config = json.load(openfile)
            self.window["-ID-"].update(
                values=[], value="Loading...", visible=True, disabled=True
            )
            self.window["-RELOAD-"].update(disabled=True)
            if 'TEAM' in config.keys():
                self.matches = League().get_ready_matches(config['TEAM'])
            else:
                self.matches = League().get_ready_matches()
            if self.matches == {}:
                self.window["-ID-"].update(
                    values=[], value="No Matches Today", visible=True, disabled=True
                )
            else:
                self.window["-ID-"].update(
                    values=[self.matches[x] for x in self.matches],
                    value="Select Match",
                    visible=True,
                    disabled=False,
                )
            self.window["-RELOAD-"].update(disabled=False)
        except Exception as e:
            while "window" not in locals()["self"].__dict__:
                pass
            else:
                print("OK",e)
                self.window["-ERROR-"].update(
                    value="No configuration found", visible=True
                )

    def start_match(self):
        if self.streamer.test_connection() == "ERROR":
            self.window["-ERROR-"].update(
                "{} is closed or not configured".format("OBS" if self.is_obs else "vMix"), text_color="red", visible=True
            )
        else:
            self.window["-ERROR-"].update("Starting", text_color="green", visible=True)
            self.match = Match(
                list(self.matches.keys())[
                    list(self.matches.values()).index(self.values["-ID-"])
                ],
                self.window,
            )
            self.court = Court(self.match)
            self.court.start()
