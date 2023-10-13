from theme import *
import PySimpleGUI as sg
import json

DOMAINS = {
    "LIVOSUR": "https://livosur-web.dataproject.com",
    "VOLLEYBALL DANMARK": "https://dvbf-web.dataproject.com",
    "Baltic League": "https://bvl-web.dataproject.com",
    "Federacion del Voleibol Argentino": "https://aclav-web.dataproject.com",
    "Federacion Metropolitana de Voleibol": "https://fmv-web.dataproject.com",
    "National Volleyball League": "https://bvf-web.dataproject.com",
    "Lotto": "https://www.euromillionsvolleyleague.be/",
    "NLB": "https://swi-web.dataproject.com",
    "Federacion Metropolitana de Voleibol":"https://fmv-web.dataproject.com",
    "Slovenská Volejbalová Federácia":"https://svf-web.dataproject.com",
    "Malta Volleyball Association":"https://mva-web.dataproject.com",
    "OZS":"https://mva-web.dataproject.com",
    "Real Federación Española de Voleibol":"https://rfevb-web.dataproject.com",
    "Svensk Volleyboll":"https://svbf-web.dataproject.com",
    "Türkiye Voleybol Federasyonu":"https://tvf-web.dataproject.com",
    "BLAKSAMBAND ÍSLANDS":"https://bli-web.dataproject.com",
    "MESTARUUSLIIGA":"https://lml-web.dataproject.com",
    "Argelian Volleyball Federation":"https://favb-web.dataproject.com",
    "Flogboltssamband Foeroya":"https://fbf-web.dataproject.com",
    "Norges Volleyballforbund":"https://nvbf-web.dataproject.com",
    "Czech Volleyball Federation":"https://cvf-web.dataproject.com",
    "Lotto":"https://bevl-web.dataproject.com",
    "Confederação Brasileira de Voleibol":"https://cbv-web.dataproject.com",
    }

class LeagueConfig():
    def __init__(self):
        T_league = [[sg.Text("Liga")]]
        S_league = [[sg.Combo([x for x in DOMAINS], default_value='Elegir liga', key='-LEAGUE-',
                            auto_size_text=True, enable_events=True, expand_x=True, expand_y=True, size=(30,10),readonly = True)]]
        T_Save = [[sg.Text("Guardado", key="-SAVE_TXT-", visible=False)]]
        B_Save= [[sg.Button("Guardar", key="-SAVE-")]]
        layout = [
                    [sg.Column(T_league, element_justification='c', expand_x=True, expand_y=True),sg.Column(S_league, element_justification='c', expand_x=True, expand_y=True)],
                    [sg.HorizontalSeparator(pad=(10,10))],
                    [sg.Column(B_Save, element_justification='c', expand_x=True, expand_y=True),sg.Column(T_Save, element_justification='c', expand_x=True, expand_y=True)]
                ]
        self.window = sg.Window("LivoStream - League Config", icon=logo,
                        layout=layout, font=("Bebas", 15), auto_size_text = True, auto_size_buttons = True, modal= True,resizable=True, finalize=True)
        try:
            self.get_config()
        except Exception as e:
            sg.Popup('Configurar', keep_on_top=True)

        while True:
            event, values = self.window.read()
            if event == '-SAVE-':
                self.save_config()
                self.window.write_event_value('-RELOAD-','')
                
            elif event == "Exit" or event == sg.WIN_CLOSED:
                break
            
        self.window.close()
    def get_config(self):
        with open('./Config/api_config.json', 'r') as openfile:
            # Reading from json file
            config = json.load(openfile)
            self.window['-LEAGUE-'].update(value=list(DOMAINS.keys())[list(DOMAINS.values()).index(config['LEAGUE_URL'])], visible=True)

    def save_config(self):
        self.window['-SAVE_TXT-'].update(visible=False)
        event, values = self.window.read()
        # Data to be written
        dictionary = {
            "LEAGUE_URL": DOMAINS[values['-LEAGUE-']],
            "LEAGUE": DOMAINS[values['-LEAGUE-']].replace('https://','').replace('-web.dataproject.com',''),
        }
        
        # Serializing json
        json_object = json.dumps(dictionary, indent=4)
        with open("./Config/api_config.json", "w") as outfile:
            outfile.write(json_object)
            self.window['-SAVE_TXT-'].update(visible=True)
            pass
        return True
