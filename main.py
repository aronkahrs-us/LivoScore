import PySimpleGUI as sg
import threading
import json
import time
import base64
import platform, os, sys
from theme import *
from config_elements import ElementsConfig
from config_stream import StreamConfig
from config_league import LeagueConfig
from Utils.obs import Obs
from Utils.vmix import Vmix
from Utils.apiv3 import Match
from Utils.league import League
from Utils.court import Court
from Utils.auth import Auth
from Utils.remote import Remote


class Main:
    """GUI and main responsabilities like starting the match and the nessesary configuration"""
    def __init__(self) -> None:
        """Init of Main"""
        try:
            with open("./lic.lvs", "r") as lic:
                data = lic.read().encode("utf-16")
                data = base64.b64decode(data).decode("utf-16")
                data = json.loads(data)
                self.client = data["user"]
                self.token = data["token"]
                if not Auth(self.client, self.token).is_authorized():
                    sg.popup(
                        "No autorizado o sin conexion a internet", title="Not Autorized"
                    )
                    sys.exit("No autorizado o sin conexion a internet")
        except Exception as e:
            print(e)
            sg.popup(
                'No se encontro licencia, asegurese tener el archivo "lic.lvs" junto a su programa',
                title="Licencia no encontrada",
            )
            sys.exit("Licencia no encontrada")
        try:
            # Gets the streamer configuration and sets it
            with open("./Config/stream_config.json", "r") as openfile:
                config = json.load(openfile)
                self.is_obs = config["OBS"]
                self.is_vmix = config["VMIX"]
                self.streamer = Obs() if self.is_obs else Vmix()
        except Exception as e:
            # If couldn't connect to streamer
            if "streamer" in locals()["self"].__dict__ and self.streamer.inputs == {}:
                sg.popup(
                    "Check that OBS is open!"
                    if self.is_obs
                    else "Check that OBS is open!"
                )
            else:
                # If couldn't get the configuration shows a popup
                sg.popup(f"Configuration not found, make sure to set everything up!")
        # Sets theme
        sg.theme("LIVO")
        # UI Elements
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
        B_Iniciar = [[sg.Button("Start", key="-ST-",pad=(0, 0), border_width=0, disabled=True, button_color="#002B45 on white",disabled_button_color='Gray')]]
        B_Reload = [
            [
                sg.Button(
                    "🔄", key="-RELOAD-",pad=(0, 0), button_color="white on #002B45", border_width=
                0
            )
        ]]
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
        # Main Layout
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
        # Makes the config directory, depends on the os the way to create it
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
        # Create window
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
        #####################################################################
        ################    ON DEVELOPEMENT #################################
        #####################################################################
        # remt=Remote(self.window)                                          #
        # threading.Thread(target=remt.run, daemon=True).start()            #
        # Event Loop to process "events" and get the "values" of the inputs #
        #####################################################################

        # Main Loop, handles events
        while True:
            event, self.values = self.window.read()

            if (
                event == sg.WIN_CLOSED or event == "Cancel"
            ):  # if user closes self.window or clicks cancel
                # if a match is ongoing, stops before closing
                if "match" in locals()["self"].__dict__:
                    self.match._stop(close=True)
                break
            elif (
                event == "Stream Elements"
            ):  # if user opens Elements config, checks if streaming sowtfare is available
                if self.streamer.test_connection() != "ERROR":
                    # if available then opens the Elements config
                    ElementsConfig()
                else:
                    # if unavailable shows error message
                    self.window["-ERROR-"].update(
                        "{} is closed or not configured".format(
                            "OBS" if self.is_obs else "vMix"
                        ),
                        text_color="red",
                        visible=True,
                    )
            elif event == "Stream Config":  # if user opens stream config
                StreamConfig()
            elif event == "League Config":  # if user opens League config
                LeagueConfig()
            elif (
                event == "-ID-" and self.values["-ID-"] != ""
            ):  # if match list populates
                self.window["-ST-"].update(disabled=False)
            elif event == "-ST-":  # if user starts/stops a match
                self.window["-ST-"].update(disabled=True)
                try:
                    print("try")
                    if (
                        "match" in locals()["self"].__dict__
                        and self.match.is_running == True
                    ):  # if match exists and is running, stops it
                        if self.is_obs:
                            self.court.stop()
                        self.match._stop()
                        self.match.is_running = False
                        self.window["-RELOAD-"].update(disabled=False)
                        self.window["-ST-"].update(disabled=False)
                    else:  # if match does not exist or is not runing, starts a new match
                        self.window["-RELOAD-"].update(disabled=True)
                        threading.Thread(target=self.start_match, daemon=True).start()
                except Exception as e:
                    self.window["-RELOAD-"].update(disabled=False)
                    self.window["-ST-"].update(disabled=False)
                    print("excp", e)

            elif event == "-RELOAD-":  # if user reloads matches
                threading.Thread(target=self.list_matches, daemon=True).start()
            elif event == "STARTED":  # Match started, stops "starting.." animation
                self.starting_run = False
                self.window["-ST-"].update(disabled=False)
        # Closes main window
        self.window.close()

    def list_matches(self):
        """Method to get and lists matches in the dropdown"""
        try:
            # Get league configuration
            with open("./Config/league_config.json", "r") as openfile:
                config = json.load(openfile)
            # starts loading text animation
            th = threading.Thread(
                target=self._starting, args=("-ID-", "Loading"), daemon=True
            )  # Starts animation
            th.start()
            self.window["-RELOAD-"].update(disabled=True)
            self.window["-ID-"].update(disabled=True)
            self.window["-ST-"].update(disabled=True)
            # Get the matches from the selected league, if a team is provided, then it filters only the matches of that team
            if "TEAM" in config.keys():
                self.matches = League().get_ready_matches(config["TEAM"])
            else:
                self.matches = League().get_ready_matches()
            # if there are matches, shows them in the dropdown, if not then it shows no matches and disables the dropdown
            self.starting_run = False
            th.join()
            if self.matches == {}:
                self.window["-ID-"].update(
                    values=[], value="No Matches Today", visible=True, disabled=True
                )
            else:
                self.window["-ID-"].update(
                    values=[self.matches[x]["Match"] for x in self.matches],
                    value="Select Match",
                    visible=True,
                    disabled=False,
                )
            self.window["-RELOAD-"].update(disabled=False)
            self.window["-ID-"].update(disabled=False)
        except Exception as e:
            # waits for the window to be set and shows an error
            while "window" not in locals()["self"].__dict__:
                pass
            else:
                print("OK", e)
                self.window["-ERROR-"].update(
                    value="No configuration found", visible=True
                )

    def start_match(self):
        """Method to start matches, gets the match id of the match selected in the dropdown and if streamer available creates a new match"""
        if self.streamer.test_connection() == "ERROR":
            self.window["-ERROR-"].update(
                "{} is closed or not configured".format(
                    "OBS" if self.is_obs else "vMix"
                ),
                text_color="red",
                visible=True,
            )
            self.window["-RELOAD-"].update(disabled=False)
            self.window["-ST-"].update(disabled=False)
        elif Auth(self.client, self.token).is_authorized():
            self.window["-RELOAD-"].update(disabled=True)
            self.window["-ID-"].update(disabled=True)
            self.window["-ERROR-"].update(text_color="green", visible=True)
            self.th_starting = threading.Thread(
                target=self._starting, args=("-ERROR-", "Starting"), daemon=True
            )  # Starts animation
            self.th_starting.start()
            self.match = Match(
                [
                    Id
                    for Id, Match in self.matches.items()
                    if Match["Match"] == self.values["-ID-"]
                ][0],
                [
                    Match["CompID"]
                    for Id, Match in self.matches.items()
                    if Match["Match"] == self.values["-ID-"]
                ][0],
                self.window,
            )  # creates new match
            if self.is_obs:  # if streamer is obs, starts flask server with pleayers
                self.court = Court(self.match)
                self.court.start()
            self.match.is_running = True
        else:
            sg.popup("No autorizado o sin conexion a internet", title="Not Autorized")

    def _starting(self, id, text):
        """Method to animate 'Starting...' text"""
        self.starting_run = True
        while self.starting_run:
            time.sleep(0.5)
            self.window[id].update(text)
            time.sleep(0.5)
            self.window[id].update("{}.".format(text))
            time.sleep(0.5)
            self.window[id].update("{}..".format(text))
            time.sleep(0.5)
            self.window[id].update("{}...".format(text))
