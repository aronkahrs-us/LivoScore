import os
import json
from theme import *
import PySimpleGUI as sg
from Utils.obs import Obs
from Utils.vmix import Vmix


class StreamConfig:
    """GUI for stream config and all the responsabilities related"""
    def __init__(self) -> None:
        """Init GUI and elements"""
        T_ip = [[sg.Text("Ip Address")]]
        S_ip = [[sg.Input("", enable_events=True, key="-IP-")]]
        T_port = [[sg.Text("Port")]]
        S_port = [[sg.Input("", enable_events=True, key="-PORT-")]]
        T_pass = [[sg.Text("Password")]]
        S_pass = [[sg.Input("", enable_events=True, key="-PASS-")]]
        S_obs = [[sg.Radio("OBS","stream", enable_events=True, key="-OBS-")]]
        S_vmix = [[sg.Radio("vMix","stream", enable_events=True, key="-VMIX-")]]
        T_Save = [[sg.Text("Saved", key="-SAVE_TXT-", visible=False)]]
        B_Save = [[sg.Button("Save", key="-SAVE-")]]
        B_Test = [[sg.Button("Test Connection", key="-TEST-")]]
        # Config layout
        layout = [
            [
                sg.Column(
                    T_ip, element_justification="c", expand_x=True, expand_y=True
                ),
                sg.Column(
                    S_ip, element_justification="c", expand_x=True, expand_y=True
                ),
            ],
            [
                sg.Column(
                    T_port, element_justification="c", expand_x=True, expand_y=True
                ),
                sg.Column(
                    S_port, element_justification="c", expand_x=True, expand_y=True
                ),
            ],
            [
                sg.Column(
                    T_pass, element_justification="c", expand_x=True, expand_y=True
                ),
                sg.Column(
                    S_pass, element_justification="c", expand_x=True, expand_y=True
                ),
            ],
            [
                sg.Column(
                    S_obs, element_justification="c", expand_x=True, expand_y=True
                ),
                sg.Column(
                    S_vmix, element_justification="c", expand_x=True, expand_y=True
                ),
            ],
            [
                sg.Column(
                    B_Save, element_justification="c", expand_x=True, expand_y=True
                ),
                sg.Column(
                    B_Test, element_justification="c", expand_x=True, expand_y=True
                ),
                sg.Column(
                    T_Save, element_justification="c", expand_x=True, expand_y=True
                ),
            ],
        ]
        #Starts window
        self.window = sg.Window(
            "Livoscore - Stream Config",
            icon=logo,
            layout=layout,
            font=("Bebas", 15),
            auto_size_text=True,
            auto_size_buttons=True,
            modal=True,
            resizable=True,
            finalize=True,
        )
        # get the streamer configuration, if exists
        self.get_config()
        # Stream config, handles events
        while True:
            event, self.values = self.window.read()
            if event == "-SAVE-":   # if user saves config
                self.save_config()
            elif event == "-TEST-": # if user test config
                self.test_config()
            elif event == "Exit" or event == sg.WIN_CLOSED:
                break

        self.window.close()

    def get_config(self):
        try:
            with open("./Config/stream_config.json", "r") as openfile:
                # Reading from json file
                config = json.load(openfile)
                self.window["-IP-"].update(value=config["IP"], visible=True)
                self.window["-PORT-"].update(value=config["PORT"], visible=True)
                self.window["-PASS-"].update(value=config["PASS"], visible=True)
                self.window["-OBS-"].update(value=config["OBS"], visible=True)
                self.window["-VMIX-"].update(value=config["VMIX"], visible=True)
                self.streamer = Obs() if config["OBS"] else Vmix()
        except Exception as e:
            print(e)
            sg.Popup("Configure", keep_on_top=True)

    def test_config(self):
        self.window["-SAVE_TXT-"].update(
                value="Testing...", text_color="white", visible=True
            )
        self.streamer = Obs() if self.values["-OBS-"] else Vmix()
        if self.streamer.test_connection_params(
                self.values["-IP-"], self.values["-PORT-"], self.values["-PASS-"]
            ) != "ERROR":
            self.window["-SAVE_TXT-"].update(
                value="OK", text_color="green", visible=True
            )
        else:
            self.window["-SAVE_TXT-"].update(
                value="ERROR", text_color="red", visible=True
            )

    def save_config(self):
        # Data to be written
        dictionary = {
            "IP": self.values["-IP-"],
            "PORT": self.values["-PORT-"],
            "PASS": self.values["-PASS-"],
            "OBS": self.values["-OBS-"],
            "VMIX": self.values["-VMIX-"],
        }
        # Serializing json
        json_object = json.dumps(dictionary, indent=4)
        filename = "./Config/stream_config.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as outfile:
            outfile.write(json_object)
            self.window["-SAVE_TXT-"].update(
                "Saved", text_color="white", visible=True
            )
