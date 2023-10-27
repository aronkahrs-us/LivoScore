import PySimpleGUI as sg
from Utils.obs import Obs
from Utils.vmix import Vmix
from theme import *
import json
import platform, os
from pathlib import Path


class StreamConfig:
    def __init__(self) -> None:
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
        self.get_config()

        while True:
            event, values = self.window.read()
            print(values)
            if event == "-SAVE-":
                self.save_config()
            elif event == "-TEST-":
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
        event, values = self.window.read()
        self.streamer = Obs() if values["-OBS-"] else Vmix()
        if (
            self.streamer.test_connection_params(
                values["-IP-"], values["-PORT-"], values["-PASS-"]
            )
            != "ERROR"
        ):
            self.window["-SAVE_TXT-"].update(
                value="OK", text_color="green", visible=True
            )
        else:
            self.window["-SAVE_TXT-"].update(
                value="ERROR", text_color="red", visible=True
            )

    def save_config(self):
        event, values = self.window.read()
        # Data to be written
        dictionary = {
            "IP": values["-IP-"],
            "PORT": values["-PORT-"],
            "PASS": values["-PASS-"],
            "OBS": values["-OBS-"],
            "VMIX": values["-VMIX-"],
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
