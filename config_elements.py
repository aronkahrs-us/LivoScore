import PySimpleGUI as sg
from Utils import obs
from Utils import vmix
from theme import *
import json
import os

class ElementsConfig:
    def __init__(self) -> None:
        """Init GUI and elements"""
        try:
            with open("./Config/stream_config.json", "r") as openfile:
                config = json.load(openfile)
                self.is_obs = config['OBS']
                self.is_vmix = config['VMIX']
        except Exception as e:
            print('import',e)
        scenes= obs.Obs().get_scenes() if self.is_obs else []
        T_scn = [[sg.Text("" if self.is_vmix else "Select Scene")]]
        S_scn = [
            [
                sg.Combo(
                    scenes,
                    default_value="",
                    disabled= self.is_vmix,
                    visible= self.is_obs,
                    key="-SCENE-",
                    auto_size_text=True,
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    readonly=True,
                )
            ]
        ]

        T_elmTO = [[sg.Text("Time Out", expand_x=True, expand_y=True)]]
        S_elmTO = [
            [
                sg.Combo(
                    [],
                    default_value="Select Element",
                    key="-Elm37-",
                    auto_size_text=True,
                    enable_events=True,
                    disabled=True,
                    expand_x=True,
                    expand_y=True,
                    readonly=True,
                )
            ]
        ]
        T_elmMP = [[sg.Text("Match Point", expand_x=True, expand_y=True)]]
        S_elmMP = [
            [
                sg.Combo(
                    [],
                    default_value="Select Element",
                    key="-Elm38-",
                    auto_size_text=True,
                    enable_events=True,
                    disabled=True,
                    expand_x=True,
                    expand_y=True,
                    readonly=True,
                )
            ]
        ]
        T_elmSP = [[sg.Text("Set Point", expand_x=True, expand_y=True)]]
        S_elmSP = [
            [
                sg.Combo(
                    [],
                    default_value="Select Element",
                    key="-Elm39-",
                    auto_size_text=True,
                    enable_events=True,
                    disabled=True,
                    expand_x=True,
                    expand_y=True,
                    readonly=True,
                )
            ]
        ]
        T_elmREF = [[sg.Text("Referees", expand_x=True, expand_y=True)]]
        S_elmREF = [
            [
                sg.Combo(
                    [],
                    default_value="Select Element",
                    key="-Elm40-",
                    auto_size_text=True,
                    enable_events=True,
                    disabled=True,
                    expand_x=True,
                    expand_y=True,
                    readonly=True,
                )
            ]
        ]
        T_elmSPH = [[sg.Text("Sets % Home", expand_x=True, expand_y=True)]]
        S_elmSPH = [
            [
                sg.Combo(
                    [],
                    default_value="Select Element",
                    key="-Elm41-",
                    auto_size_text=True,
                    enable_events=True,
                    disabled=True,
                    expand_x=True,
                    expand_y=True,
                    readonly=True,
                )
            ]
        ]
        T_elmPPH = [[sg.Text("Points % Home", expand_x=True, expand_y=True)]]
        S_elmPPH = [
            [
                sg.Combo(
                    [],
                    default_value="Select Element",
                    key="-Elm42-",
                    auto_size_text=True,
                    enable_events=True,
                    disabled=True,
                    expand_x=True,
                    expand_y=True,
                    readonly=True,
                )
            ]
        ]
        T_elmSPA = [[sg.Text("Sets % Away", expand_x=True, expand_y=True)]]
        S_elmSPA = [
            [
                sg.Combo(
                    [],
                    default_value="Select Element",
                    key="-Elm43-",
                    auto_size_text=True,
                    enable_events=True,
                    disabled=True,
                    expand_x=True,
                    expand_y=True,
                    readonly=True,
                )
            ]
        ]
        T_elmPPA = [[sg.Text("Points % Away", expand_x=True, expand_y=True)]]
        S_elmPPA = [
            [
                sg.Combo(
                    [],
                    default_value="Select Element",
                    key="-Elm44-",
                    auto_size_text=True,
                    enable_events=True,
                    disabled=True,
                    expand_x=True,
                    expand_y=True,
                    readonly=True,
                )
            ]
        ]
        T_elmRH = [[sg.Text("Results Home", expand_x=True, expand_y=True)]]
        S_elmRH = [
            [
                sg.Combo(
                    [],
                    default_value="Select Element",
                    key="-Elm45-",
                    auto_size_text=True,
                    enable_events=True,
                    disabled=True,
                    expand_x=True,
                    expand_y=True,
                    readonly=True,
                )
            ]
        ]
        T_elmRA = [[sg.Text("Results Away", expand_x=True, expand_y=True)]]
        S_elmRA = [
            [
                sg.Combo(
                    [],
                    default_value="Select Element",
                    key="-Elm46-",
                    auto_size_text=True,
                    enable_events=True,
                    disabled=True,
                    expand_x=True,
                    expand_y=True,
                    readonly=True,
                )
            ]
        ]
        T_elmWIN = [[sg.Text("Winner", expand_x=True, expand_y=True)]]
        S_elmWIN = [
            [
                sg.Combo(
                    [],
                    default_value="Select Element",
                    key="-Elm47-",
                    auto_size_text=True,
                    enable_events=True,
                    disabled=True,
                    expand_x=True,
                    expand_y=True,
                    readonly=True,
                )
            ]
        ]
        T_elmMHI = [[sg.Text("Match History", expand_x=True, expand_y=True)]]
        S_elmMHI = [
            [
                sg.Combo(
                    [],
                    default_value="Select Element",
                    key="-Elm48-",
                    auto_size_text=True,
                    enable_events=True,
                    disabled=True,
                    expand_x=True,
                    expand_y=True,
                    readonly=True,
                )
            ]
        ]
        T_elmPS = [[sg.Text("Player Stats", expand_x=True, expand_y=True)]]
        S_elmPS = [
            [
                sg.Combo(
                    [],
                    default_value="Select Element",
                    key="-Elm49-",
                    auto_size_text=True,
                    enable_events=True,
                    disabled=True,
                    expand_x=True,
                    expand_y=True,
                    readonly=True,
                )
            ]
        ]
        S_elmATO = [
            [
                sg.Checkbox(
                    text='Automate Time Out',
                    default=True,
                    key="-Elm50-",
                    enable_events=True,
                    disabled=True,
                )
            ]
        ]
        S_elmISF = [
            [
                sg.Checkbox(
                    text='Is Championship Final?',
                    default=True,
                    key="-Elm51-",
                    enable_events=True,
                    disabled=True,
                )
            ]
        ]
        T_Save = [[sg.Text("Saved", key="-SAVE_TXT-", visible=False)]]
        B_Save = [[sg.Button("Save", key="-SAVE-")]]
        t_main_elem = ["Name", "Logo", "Points", "Sets", "Serve", "Substitution"]
        t_stats_elem = [
            "Points %",
            "Total Points",
            "Set 1 %",
            "Set 1 Points",
            "Set 2 %",
            "Set 2 Points",
            "Set 3 %",
            "Set 3 Points",
            "Set 4 %",
            "Set 4 Points",
            "Set 5 %",
            "Set 5 Points",
        ]
        main_layout = []
        stats_layout = []
        stats2_layout = [[
            sg.Column(
                    T_elmSPH, element_justification="left", expand_x=True, expand_y=True
                ),
            sg.Column(
                    S_elmSPH, element_justification="left", expand_x=True, expand_y=True
                ),
            sg.Column(
                    T_elmSPA, element_justification="left", expand_x=True, expand_y=True
                ),
            sg.Column(
                    S_elmSPA, element_justification="left", expand_x=True, expand_y=True
                ),
        ],[
            sg.Column(
                    T_elmPPH, element_justification="left", expand_x=True, expand_y=True
                ),
            sg.Column(
                    S_elmPPH, element_justification="left", expand_x=True, expand_y=True
                ),
            sg.Column(
                    T_elmPPA, element_justification="left", expand_x=True, expand_y=True
                ),
            sg.Column(
                    S_elmPPA, element_justification="left", expand_x=True, expand_y=True
                ),
        ],[
            sg.Column(
                    T_elmRH, element_justification="left", expand_x=True, expand_y=True
                ),
            sg.Column(
                    S_elmRH, element_justification="left", expand_x=True, expand_y=True
                ),
            sg.Column(
                    T_elmRA, element_justification="left", expand_x=True, expand_y=True
                ),
            sg.Column(
                    S_elmRA, element_justification="left", expand_x=True, expand_y=True
                ),
        ],[
            sg.Column(
                    T_elmWIN, element_justification="left", expand_x=True, expand_y=True
                ),
            sg.Column(
                    S_elmWIN, element_justification="left", expand_x=True, expand_y=True
                ),
            sg.Column(
                    T_elmMHI, element_justification="left", expand_x=True, expand_y=True
                ),
            sg.Column(
                    S_elmMHI, element_justification="left", expand_x=True, expand_y=True
                ),
        ],[
            sg.Column(
                    T_elmPS, element_justification="left", expand_x=True, expand_y=True
                ),
            sg.Column(
                    S_elmPS, element_justification="left", expand_x=True, expand_y=True
                ),
        ]]
        misc_layout = [
            [
            sg.Column(
                    S_elmATO, element_justification="left", expand_x=True, expand_y=True
                ),
            sg.Column(
                    S_elmISF, element_justification="left", expand_x=True, expand_y=True
                ),
        ]
        ]
        self.n = 1
        for i in t_main_elem:
            main_layout.append(
                [
                    sg.Column(
                        [[sg.Text("Home " + i, expand_x=True, expand_y=True)]],
                        element_justification="left",
                        expand_x=True,
                        expand_y=True,
                    ),
                    sg.Column(
                        [
                            [
                                sg.Combo(
                                    [],
                                    default_value="Select Element",
                                    key="-Elm{}-".format(self.n),
                                    auto_size_text=True,
                                    enable_events=True,
                                    disabled=True,
                                    expand_x=True,
                                    expand_y=True,
                                    readonly=True,
                                )
                            ]
                        ],
                        element_justification="left",
                        expand_x=True,
                        expand_y=True,
                    ),
                    sg.Column(
                        [[sg.Text("Away " + i, expand_x=True, expand_y=True)]],
                        element_justification="left",
                        expand_x=True,
                        expand_y=True,
                    ),
                    sg.Column(
                        [
                            [
                                sg.Combo(
                                    [],
                                    default_value="Select Element",
                                    key="-Elm{}-".format(self.n + 1),
                                    auto_size_text=True,
                                    enable_events=True,
                                    disabled=True,
                                    expand_x=True,
                                    expand_y=True,
                                    readonly=True,
                                )
                            ]
                        ],
                        element_justification="left",
                        expand_x=True,
                        expand_y=True,
                    ),
                ]
            )
            self.n += 2
        main_layout.append(
            [
                sg.Column(
                    T_elmMP, element_justification="left", expand_x=True, expand_y=True
                ),
                sg.Column(
                    S_elmMP, element_justification="left", expand_x=True, expand_y=True
                ),
                sg.Column(
                    T_elmSP, element_justification="left", expand_x=True, expand_y=True
                ),
                sg.Column(
                    S_elmSP, element_justification="left", expand_x=True, expand_y=True
                ),
            ]
        )
        main_layout.append(
            [
                sg.Column(
                    T_elmTO, element_justification="left", expand_x=True, expand_y=True
                ),
                sg.Column(
                    S_elmTO, element_justification="left", expand_x=True, expand_y=True
                ),
                sg.Column(
                    T_elmREF, element_justification="left", expand_x=True, expand_y=True
                ),
                sg.Column(
                    S_elmREF, element_justification="left", expand_x=True, expand_y=True
                ),
            ]
        )
        for i in t_stats_elem:
            stats_layout.append(
                [
                    sg.Column(
                        [[sg.Text("Home " + i, expand_x=True, expand_y=True)]],
                        element_justification="left",
                        expand_x=True,
                        expand_y=True,
                    ),
                    sg.Column(
                        [
                            [
                                sg.Combo(
                                    [],
                                    default_value="Select Element",
                                    key="-Elm{}-".format(self.n),
                                    auto_size_text=True,
                                    enable_events=True,
                                    disabled=True,
                                    expand_x=True,
                                    expand_y=True,
                                    readonly=True,
                                )
                            ]
                        ],
                        element_justification="left",
                        expand_x=True,
                        expand_y=True,
                    ),
                    sg.Column(
                        [[sg.Text("Away " + i, expand_x=True, expand_y=True)]],
                        element_justification="left",
                        expand_x=True,
                        expand_y=True,
                    ),
                    sg.Column(
                        [
                            [
                                sg.Combo(
                                    [],
                                    default_value="Select Element",
                                    key="-Elm{}-".format(self.n + 1),
                                    auto_size_text=True,
                                    enable_events=True,
                                    disabled=True,
                                    expand_x=True,
                                    expand_y=True,
                                    readonly=True,
                                )
                            ]
                        ],
                        element_justification="left",
                        expand_x=True,
                        expand_y=True,
                    ),
                ]
            )
            self.n += 2
        layout = [
            [
                sg.Column(
                    T_scn, element_justification="left", expand_x=True, expand_y=True
                ),
                sg.Column(
                    S_scn, element_justification="left", expand_x=True, expand_y=True
                ),
            ],
            [sg.HorizontalSeparator(pad=(10, 10))],
            [
                sg.TabGroup(
                    [[sg.Tab("Main", main_layout), sg.Tab("Stats", stats_layout), sg.Tab("Stats 2", stats2_layout), sg.Tab("Misc", misc_layout)]],
                    s=(750, 450),
                    expand_x=True,
                    expand_y=True,
                )
            ],
            [
                sg.Column(
                    B_Save, element_justification="left", expand_x=True, expand_y=True
                ),
                sg.Column(
                    T_Save, element_justification="left", expand_x=True, expand_y=True
                ),
            ],
        ]
        self.window = sg.Window(
            "Livoscore - Config",
            icon=logo,
            layout=layout,
            font=("Bebas", 15),
            auto_size_text=True,
            auto_size_buttons=True,
            modal=True,
            resizable=True,
            finalize=True,
            size=(800, 600),
        )
        self.get_config()
        while True:
            event, self.values = self.window.read()
            if event == "-SCENE-":
                self.get_elements(self.values["-SCENE-"])
            elif event == "-SAVE-":
                self.save_config()
            elif event == "Exit" or event == sg.WIN_CLOSED:
                break

        self.window.close()

    def get_config(self):
        """Get config from file"""
        try:
            with open("./Config/elem_config.json", "r") as openfile:
                # Reading from json file
                config = json.load(openfile)
                items = self.get_elements(config["SCENE"]) if self.is_obs else self.get_elements()
                x=1
                if items != "ERROR":
                    for key in config:
                        if key == "SCENE":
                            self.window["-" + key + "-"].update(
                                value=config[key]
                            )
                        else:
                            # self.window['-Elm'+str(x)+'-'].update(value=list(items.keys())[list(items.values()).index(config[key])], visible=True, disabled=False)
                            # print(type(config[key]),x)
                            if type(config[key]) == str:
                                self.window["-Elm" + str(x) + "-"].update(
                                    value=config[key], visible=True, disabled=False
                                )
                            elif type(config[key]) == dict:
                                self.window["-Elm" + str(x) + "-"].update(
                                    value=config[key]['name'], visible=True, disabled=False
                                )
                            elif type(config[key]) == bool:
                                self.window["-Elm" + str(x) + "-"].update(
                                    value=config[key], visible=True, disabled=False
                                )
                            else:
                                self.window["-Elm" + str(x) + "-"].update(
                                    value=[
                                        name
                                        for name, element in items.items()
                                        if element.get("id") == config[key]
                                    ][0],
                                    visible=True,
                                    disabled=False,
                                )
                        x+=1
        except Exception as e:
            print('error voy a try 2: ',e)
            try:
                if self.is_vmix:
                    self.get_elements()
                else:
                    print(e)
                    sg.Popup("Configurar", keep_on_top=True)
            except Exception as e:
                print(e)
                sg.Popup("Configurar", keep_on_top=True)

    def get_elements(self, scene=None) -> list:
        """Get elements from streamer"""
        items = obs.Obs().get_scene_items(scene) if self.is_obs else vmix.Vmix()._get_inputs()
        if items != "ERROR":
            elements = []
            for x in items:
                elements.append(x)
            for x in range(1, self.n + 15):
                try:
                    self.window["-Elm" + str(x) + "-"].update(
                        value="Select", values=elements, visible=True, disabled=False
                    )
                except:
                    self.window["-Elm" + str(x) + "-"].update(visible=True, disabled=False)
        return items

    def save_config(self):
        """Save config to file"""
        elements = obs.Obs().get_scene_items(self.values["-SCENE-"]) if self.is_obs else vmix.Vmix()._get_inputs()
        if elements != "ERROR":
            # Data to be written
            if self.is_vmix:
                dictionary = {
                    "HOME_NAME": elements[self.values["-Elm1-"]],
                    "AWAY_NAME": elements[self.values["-Elm2-"]],
                    "HOME_LOGO": elements[self.values["-Elm3-"]],
                    "AWAY_LOGO": elements[self.values["-Elm4-"]],
                    "HOME_POINTS": elements[self.values["-Elm5-"]],
                    "AWAY_POINTS": elements[self.values["-Elm6-"]],
                    "HOME_SET": elements[self.values["-Elm7-"]],
                    "AWAY_SET": elements[self.values["-Elm8-"]],
                    "H_SERVE": elements[self.values["-Elm9-"]],
                    "A_SERVE": elements[self.values["-Elm10-"]],
                    "H_SUBSTITUTION": elements[self.values["-Elm11-"]],
                    "A_SUBSTITUTION": elements[self.values["-Elm12-"]],
                    "HOME_STATS_PT": elements[self.values["-Elm13-"]],
                    "AWAY_STATS_PT": elements[self.values["-Elm14-"]],
                    "HOME_STATS_PuntosT": elements[self.values["-Elm15-"]],
                    "AWAY_STATS_PuntosT": elements[self.values["-Elm16-"]],
                    "HOME_STATS_P1": elements[self.values["-Elm17-"]],
                    "AWAY_STATS_P1": elements[self.values["-Elm18-"]],
                    "HOME_STATS_S1": elements[self.values["-Elm19-"]],
                    "AWAY_STATS_S1": elements[self.values["-Elm20-"]],
                    "HOME_STATS_P2": elements[self.values["-Elm21-"]],
                    "AWAY_STATS_P2": elements[self.values["-Elm22-"]],
                    "HOME_STATS_S2": elements[self.values["-Elm23-"]],
                    "AWAY_STATS_S2": elements[self.values["-Elm24-"]],
                    "HOME_STATS_P3": elements[self.values["-Elm25-"]],
                    "AWAY_STATS_P3": elements[self.values["-Elm26-"]],
                    "HOME_STATS_S3": elements[self.values["-Elm27-"]],
                    "AWAY_STATS_S3": elements[self.values["-Elm28-"]],
                    "HOME_STATS_P4": elements[self.values["-Elm29-"]],
                    "AWAY_STATS_P4": elements[self.values["-Elm30-"]],
                    "HOME_STATS_S4": elements[self.values["-Elm31-"]],
                    "AWAY_STATS_S4": elements[self.values["-Elm32-"]],
                    "HOME_STATS_P5": elements[self.values["-Elm33-"]],
                    "AWAY_STATS_P5": elements[self.values["-Elm34-"]],
                    "HOME_STATS_S5": elements[self.values["-Elm35-"]],
                    "AWAY_STATS_S5": elements[self.values["-Elm36-"]],
                    "TIME_OUT": elements[self.values["-Elm37-"]],
                    "MATCH_POINT": elements[self.values["-Elm38-"]],
                    "SET_POINT": elements[self.values["-Elm39-"]],
                    "REFEREES": elements[self.values["-Elm40-"]],
                    "SP_STAT_H": elements[self.values["-Elm41-"]],
                    "PP_STAT_H": elements[self.values["-Elm42-"]],
                    "SP_STAT_A": elements[self.values["-Elm43-"]],
                    "PP_STAT_A": elements[self.values["-Elm44-"]],
                    "RESULTS_H": elements[self.values["-Elm45-"]],
                    "RESULTS_A": elements[self.values["-Elm46-"]],
                    "WINNER": elements[self.values["-Elm47-"]],
                    "MATCH_HISTORY": elements[self.values["-Elm48-"]],
                    "PLAYER_STATS": elements[self.values["-Elm49-"]],
                    "AUTOMATE_TIME_OUT": self.values["-Elm50-"],
                    "IS_FINAL": self.values["-Elm51-"],
                }
            elif self.is_obs:
                dictionary = {
                    "SCENE": self.values["-SCENE-"],
                    "HOME_NAME": elements[self.values["-Elm1-"]]["name"],
                    "AWAY_NAME": elements[self.values["-Elm2-"]]["name"],
                    "HOME_LOGO": elements[self.values["-Elm3-"]]["name"],
                    "AWAY_LOGO": elements[self.values["-Elm4-"]]["name"],
                    "HOME_POINTS": elements[self.values["-Elm5-"]]["name"],
                    "AWAY_POINTS": elements[self.values["-Elm6-"]]["name"],
                    "HOME_SET": elements[self.values["-Elm7-"]]["name"],
                    "AWAY_SET": elements[self.values["-Elm8-"]]["name"],
                    "H_SERVE": elements[self.values["-Elm9-"]]["id"],
                    "A_SERVE": elements[self.values["-Elm10-"]]["id"],
                    "H_SUBSTITUTION": elements[self.values["-Elm11-"]]["id"],
                    "A_SUBSTITUTION": elements[self.values["-Elm12-"]]["id"],
                    "HOME_STATS_PT": elements[self.values["-Elm13-"]]["name"],
                    "AWAY_STATS_PT": elements[self.values["-Elm14-"]]["name"],
                    "HOME_STATS_PuntosT": elements[self.values["-Elm15-"]]["name"],
                    "AWAY_STATS_PuntosT": elements[self.values["-Elm16-"]]["name"],
                    "HOME_STATS_P1": elements[self.values["-Elm17-"]]["name"],
                    "AWAY_STATS_P1": elements[self.values["-Elm18-"]]["name"],
                    "HOME_STATS_S1": elements[self.values["-Elm19-"]]["name"],
                    "AWAY_STATS_S1": elements[self.values["-Elm20-"]]["name"],
                    "HOME_STATS_P2": elements[self.values["-Elm21-"]]["name"],
                    "AWAY_STATS_P2": elements[self.values["-Elm22-"]]["name"],
                    "HOME_STATS_S2": elements[self.values["-Elm23-"]]["name"],
                    "AWAY_STATS_S2": elements[self.values["-Elm24-"]]["name"],
                    "HOME_STATS_P3": elements[self.values["-Elm25-"]]["name"],
                    "AWAY_STATS_P3": elements[self.values["-Elm26-"]]["name"],
                    "HOME_STATS_S3": elements[self.values["-Elm27-"]]["name"],
                    "AWAY_STATS_S3": elements[self.values["-Elm28-"]]["name"],
                    "HOME_STATS_P4": elements[self.values["-Elm29-"]]["name"],
                    "AWAY_STATS_P4": elements[self.values["-Elm30-"]]["name"],
                    "HOME_STATS_S4": elements[self.values["-Elm31-"]]["name"],
                    "AWAY_STATS_S4": elements[self.values["-Elm32-"]]["name"],
                    "HOME_STATS_P5": elements[self.values["-Elm33-"]]["name"],
                    "AWAY_STATS_P5": elements[self.values["-Elm34-"]]["name"],
                    "HOME_STATS_S5": elements[self.values["-Elm35-"]]["name"],
                    "AWAY_STATS_S5": elements[self.values["-Elm36-"]]["name"],
                    "TIME_OUT": elements[self.values["-Elm37-"]]["id"],
                    "MATCH_POINT": elements[self.values["-Elm38-"]]["id"],
                    "SET_POINT": elements[self.values["-Elm39-"]]["id"],
                }

            # Serializing json
            json_object = json.dumps(dictionary, indent=4)
            filename = "./Config/elem_config.json"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as outfile:
                outfile.write(json_object)
                self.window["-SAVE_TXT-"].update(
                    "Saved", text_color="white", visible=True
                )
