from theme import *
import PySimpleGUI as sg
import json
import os

DOMAINS = {
    "LIVOSUR": "https://livosur-web.dataproject.com",
    "VOLLEYBALL DANMARK": "https://dvbf-web.dataproject.com",
    "Baltic League": "https://bvl-web.dataproject.com",
    "Asociacion de Clubes Liga Argentina de Voleibol": "https://aclav-web.dataproject.com",
    "Federacion del Voleibol Argentino": "https://feva-web.dataproject.com",
    "Federacion Metropolitana de Voleibol": "https://fmv-web.dataproject.com",
    "National Volleyball League": "https://bvf-web.dataproject.com",
    "NLB": "https://swi-web.dataproject.com",
    "Slovenská Volejbalová Federácia": "https://svf-web.dataproject.com",
    "Malta Volleyball Association": "https://mva-web.dataproject.com",
    "OZS": "https://ozs-web.dataproject.com",
    "Real Federación Española de Voleibol": "https://rfevb-web.dataproject.com",
    "Svensk Volleyboll": "https://svbf-web.dataproject.com",
    "Türkiye Voleybol Federasyonu": "https://tvf-web.dataproject.com",
    "BLAKSAMBAND ÍSLANDS": "https://bli-web.dataproject.com",
    "MESTARUUSLIIGA": "https://lml-web.dataproject.com",
    "Argelian Volleyball Federation": "https://favb-web.dataproject.com",
    "Flogboltssamband Foeroya": "https://fbf-web.dataproject.com",
    "Norges Volleyballforbund": "https://nvbf-web.dataproject.com",
    "Czech Volleyball Federation": "https://cvf-web.dataproject.com",
    "Lotto": "https://bevl-web.dataproject.com",
    "Confederação Brasileira de Voleibol": "https://cbv-web.dataproject.com",
    "LNV": "https://lnv-web.dataproject.com",
    "Qatar Volleyball Association": "https://qva-web.dataproject.com",
    "Lithuanian Volleyball Federation": "https://lvf-web.dataproject.com",
    "Israeli Volleyball Association": "https://iva-web.dataproject.com",
    "Federata Shqiptare e Volejbollit": "https://fshv-web.dataproject.com",
    "Federația Română de Volei": "https://frv-web.dataproject.com",
    "Professional Volleyball League of Ukraine": "https://pvlu-web.dataproject.com",
    "Federacion Peruana de Voley": "https://fpdv-web.dataproject.com",
    "BIH Volley": "https://osbih-web.dataproject.com",
    "Cyprus Volleyball Association": "https://kop-web.dataproject.com",
    "HELLENIC VOLLEYBALL FEDERATION": "https://eope-web.dataproject.com",
    "Philippine Superliga": "https://psl-web.dataproject.com",
    "ODBOJKAŠKI SAVEZ SRBIJE": "https://ossrb-web.dataproject.com",
    "Federação Portuguesa de Voleibol": "https://fpv-web.dataproject.com",
    "Estonian Volleyball Federation": "https://evf-web.dataproject.com",
    "Hellenic Volleyball League": "https://hvl-web.dataproject.com",
    "Volleyball Federation of Republic of Kazakhstan": "https://vfrk-web.dataproject.com",
    "Federata e Volejbollit e Kosovës": "https://fvkos-web.dataproject.com",
    "Ukrainian Volleyball Federation": "https://uvf-web.dataproject.com",
    "Croatian Volleyball Federation": "https://hos-web.dataproject.com",
    "Federación Cordobesa de Voleibol": "https://fcv-web.dataproject.com",
    "Latvijas volejbola federācija": "https://latvf-web.dataproject.com",
    "Hungarian Volleyball Federation": "https://hvf-web.dataproject.com",
    "Middle European League": "https://mevza-web.dataproject.com",
    "Bundesliga": "https://vbl-web.dataproject.com",
}


class LeagueConfig:
    def __init__(self):
        """Init GUI and elements"""
        T_league = [[sg.Text("League")]]
        S_league = [
            [
                sg.Combo(
                    [x for x in DOMAINS],
                    default_value="Select League",
                    key="-LEAGUE-",
                    auto_size_text=True,
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    size=(30, 10),
                    readonly=True,
                )
            ]
        ]
        T_team = [[sg.Text("Team")]]
        S_team = [
            [
                sg.Input(
                    default_text="Name of the Team (optional)",
                    key="-TEAM-",
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    disabled=True,
                    size=(30, 10),
                )
            ]
        ]
        C_team = [
            [
                sg.Checkbox(
                    text='',
                    default=False,
                    enable_events=True,
                    key="-CHECK-TEAM-",
                    expand_x=True,
                    expand_y=True,
                )
            ]
        ]
        T_Save = [[sg.Text("Saved", key="-SAVE_TXT-", visible=False)]]
        B_Save = [[sg.Button("Save", key="-SAVE-")]]
        layout = [
            [
                sg.Column(
                    T_league, element_justification="c", expand_x=True, expand_y=True
                ),
                sg.Column(
                    S_league, element_justification="c", expand_x=True, expand_y=True
                ),
            ],
            [
                sg.Column(
                    T_team, element_justification="c", expand_x=True, expand_y=True
                ),
                sg.Column(
                    S_team, element_justification="c", expand_x=True, expand_y=True
                ),
                sg.Column(
                    C_team, element_justification="c", expand_x=True, expand_y=True
                ),
            ],
            [
                sg.Column(
                    B_Save, element_justification="c", expand_x=True, expand_y=True
                ),
                sg.Column(
                    T_Save, element_justification="c", expand_x=True, expand_y=True
                ),
            ],
        ]
        self.window = sg.Window(
            "Livoscore - League Config",
            icon=logo,
            layout=layout,
            font=("Bebas", 15),
            auto_size_text=True,
            auto_size_buttons=True,
            modal=True,
            resizable=True,
            finalize=True,
        )
        try:
            self.get_config()
        except Exception as e:
            print(e)
            sg.Popup("Configure", keep_on_top=True)

        while True:
            event, self.values = self.window.read()
            if event == "-SAVE-":
                self.save_config()
                self.window.write_event_value("-RELOAD-", "")
            if event == "-CHECK-TEAM-":
                self.window["-TEAM-"].update(disabled=not self.values['-CHECK-TEAM-'])

            elif event == "Exit" or event == sg.WIN_CLOSED:
                break

        self.window.close()

    def get_config(self):
        """Get config from file"""
        with open("./Config/league_config.json", "r") as openfile:
            # Reading from json file
            config = json.load(openfile)
            self.window["-LEAGUE-"].update(
                value=list(DOMAINS.keys())[
                    list(DOMAINS.values()).index(config["LEAGUE_URL"])
                ],
                visible=True,
            )
            if 'TEAM' in config.keys():
                self.window["-TEAM-"].update(value=config['TEAM'])
                self.window["-TEAM-"].update(disabled=False)
                self.window["-CHECK-TEAM-"].update(value=True)

    def save_config(self) -> bool:
        """Save config to file"""
        self.window["-SAVE_TXT-"].update(visible=False)
        # Data to be written
        if self.values['-CHECK-TEAM-']:
            dictionary = {
                "LEAGUE_URL": DOMAINS[self.values["-LEAGUE-"]],
                "LEAGUE": DOMAINS[self.values["-LEAGUE-"]]
                .replace("https://", "")
                .replace("-web.dataproject.com", ""),
                "TEAM": str(self.values["-TEAM-"]).lower()
            }
        else:
            dictionary = {
                "LEAGUE_URL": DOMAINS[self.values["-LEAGUE-"]],
                "LEAGUE": DOMAINS[self.values["-LEAGUE-"]]
                .replace("https://", "")
                .replace("-web.dataproject.com", ""),
            }

        # Serializing json
        json_object = json.dumps(dictionary, indent=4)
        filename = "./Config/league_config.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as outfile:
            outfile.write(json_object)
            self.window["-SAVE_TXT-"].update(visible=True)
        return True
