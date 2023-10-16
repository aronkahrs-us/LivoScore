from theme import *
import PySimpleGUI as sg
import json

DOMAINS = {
    "LIVOSUR": "https://livosur-web.dataproject.com",
    "VOLLEYBALL DANMARK": "https://dvbf-web.dataproject.com",
    "Baltic League": "https://bvl-web.dataproject.com",
    "Asociacion de Clubes Liga Argentina de Voleibol": "https://aclav-web.dataproject.com",
    "Federacion del Voleibol Argentino": "https://feva-web.dataproject.com",
    "Federacion Metropolitana de Voleibol": "https://fmv-web.dataproject.com",
    "National Volleyball League": "https://bvf-web.dataproject.com",
    "NLB": "https://swi-web.dataproject.com",
    "Slovenská Volejbalová Federácia":"https://svf-web.dataproject.com",
    "Malta Volleyball Association":"https://mva-web.dataproject.com",
    "OZS":"https://ozs-web.dataproject.com",
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
    "LNV":"https://lnv-web.dataproject.com",
    "Qatar Volleyball Association": "https://qva-web.dataproject.com",
    "Lithuanian Volleyball Federation":"https://lvf-web.dataproject.com",
    "Israeli Volleyball Association":"https://iva-web.dataproject.com",
    "Federata Shqiptare e Volejbollit":"https://fshv-web.dataproject.com",
    "Federația Română de Volei":"https://frv-web.dataproject.com",
    "Professional Volleyball League of Ukraine":"https://pvlu-web.dataproject.com",
    "Federacion Peruana de Voley":"https://fpdv-web.dataproject.com",
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
    "Middle European League": "https://mevza-web.dataproject.com"
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
                    [sg.Column(B_Save, element_justification='c', expand_x=True, expand_y=True),sg.Column(T_Save, element_justification='c', expand_x=True, expand_y=True)]
                ]
        self.window = sg.Window("Livoscore - League Config", icon=logo,
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
