import requests
import time
import json
import os
import threading
import PySimpleGUI as sg
from .team import Team
from .obs import Obs
from .vmix import Vmix
from .stats import Stats
from sseclient import SSEClient


class Match:
    def __init__(self, m_id, window):
        self.m_id = int(m_id)
        self.is_running = True
        self.set_point = False
        self.match_point = False
        self.window = window
        self.stats = Stats()
        try:
            with open("./Config/league_config.json", "r") as openfile:
                # Reading from json file
                config = json.load(openfile)
                self.league = config["LEAGUE"]
                self.league_url = config["LEAGUE_URL"]
        except Exception as e:
            sg.popup_error(f"AN EXCEPTION OCCURRED!", e)
        try:
            with open("./Config/stream_config.json", "r") as openfile:
                # Reading from json file
                config = json.load(openfile)
                self.is_obs = config["OBS"]
                self.is_vmix = config["VMIX"]
                self.streamer = Obs() if self.is_obs else Vmix()
        except Exception as e:
            sg.popup_error(f"AN EXCEPTION OCCURRED!", e)
        try:
            with open("./Config/elem_config.json", "r") as openfile:
                # Reading from json file
                self.elements = json.load(openfile)
        except:
            self.elements = {}
        self._get_credentials()
        self.cookies = {
            "ARRAffinitySameSite": "d4cf45d89d11a6d9b07a5dbd364ea4432ecfd8782dd6765a42a25cf772133186",
        }
        self.headers = {
            "Accept": "text/plain, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": self.league_url,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
        }
        self.negotiate()
        threading.Thread(target=self.connect).start()
        # self.connect()

    def negotiate(self):
        params = {
            "clientProtocol": "1.5",
            "connectionData": '[{"name":"signalrlivehubfederations"}]',
            "_": str(round(time.time() * 1000)),
        }

        response = requests.get(
            "https://dataprojectservicesignalr.azurewebsites.net/signalr/negotiate",
            params=params,
            cookies=self.cookies,
            headers=self.headers,
        ).json()
        self.token = response["ConnectionToken"]

    def connect(self):
        headers = {
            "Accept": "text/event-stream",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Origin": self.league_url,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
        }

        params = {
            "transport": "serverSentEvents",
            "clientProtocol": "1.5",
            "connectionToken": self.token,
            "connectionData": '[{"name":"signalrlivehubfederations"}]',
            "tid": "1",
        }

        # Create an SSE clients
        messages = SSEClient(
            "https://dataprojectservicesignalr.azurewebsites.net/signalr/connect",
            params=params,
            cookies=self.cookies,
            headers=headers,
        )
        self.start()
        self.send()
        # Iterate through SSE events
        x = 0
        for msg in messages:
            if self.is_running == False:
                print("STOP")
                break
            try:
                data = msg.data.replace("'", '"')
                if data != "initialized" and data != "{}":
                    data = json.loads(data)
                    try:
                        if data["M"][0]["M"] == "refreshPlayByPlayData":
                            self.rally = data["M"][0]["A"][0][-1]
                            self.serve = data["M"][0]["A"][0][-1]["Team"]
                            self.action = data["M"][0]["A"][0][-1]["RallyT"]
                            self.skill = data["M"][0]["A"][0][-1]["Skill"]
                            if self.action == 0 or self.action == 1:
                                threading.Thread(
                                    target=self.streamer.serve, args=self.serve
                                ).start()
                            elif self.action == 2:
                                threading.Thread(
                                    target=self.streamer.substitution, args=self.serve
                                ).start()
                            elif self.action == 3:
                                threading.Thread(target=self.streamer.time_out).start()
                        elif (
                            data["M"][0]["M"] == "updateMatchSetData_ES"
                            or data["M"][0]["M"] == "updateMatchSetData_DV"
                        ):
                            self.current_set = data["M"][0]["A"][0]["SN"]
                            self.home.points = data["M"][0]["A"][0]["HP"]
                            self.away.points = data["M"][0]["A"][0]["GP"]
                        elif (
                            data["M"][0]["M"] == "updateMatchScoreData_ES"
                            or data["M"][0]["M"] == "updateMatchScoreData_DV"
                        ):
                            self.home.sets = data["M"][0]["A"][0]["H"]
                            self.away.sets = data["M"][0]["A"][0]["G"]
                            self.status = data["M"][0]["A"][0]["S"]
                    finally:
                        if self.status == 2:
                            self._stop()
                        threading.Thread(target=self._set_point).start()
                        threading.Thread(target=self._make_statistics).start()
                        threading.Thread(target=self._update_stream).start()
                        threading.Thread(target=self._update_ui).start()

            except Exception as e:
                print(e)
                pass

    def start(self):
        params = {
            "transport": "serverSentEvents",
            "clientProtocol": "1.5",
            "connectionToken": self.token,
            "connectionData": '[{"name":"signalrlivehubfederations"}]',
            "_": str(round(time.time() * 1000)),
        }

        response = requests.get(
            "https://dataprojectservicesignalr.azurewebsites.net/signalr/start",
            params=params,
            cookies=self.cookies,
            headers=self.headers,
        ).json()

    def send(self):
        params = {
            "transport": "serverSentEvents",
            "clientProtocol": "1.5",
            "connectionToken": self.token,
            "connectionData": '[{"name":"signalrlivehubfederations"}]',
        }

        data = {
            "data": '{"H":"signalrlivehubfederations","M":"getLiveScoreListData_From_ES","A":["'
            + str(self.m_id)
            + '","'
            + self.league
            + '"],"I":0}',
        }

        data = requests.post(
            "https://dataprojectservicesignalr.azurewebsites.net/signalr/send",
            params=params,
            cookies=self.cookies,
            headers=self.headers,
            data=data,
        ).json()["R"][0]
        self.current_set = data["WonSetHome"] + data["WonSetGuest"] + 1
        if self.current_set > 5:
            self.current_set = 5
        self.home = Team(
            data["HomeEmpty"],
            data["Home"],
            data["Set" + str(self.current_set) + "Home"],
            data["WonSetHome"],
            self._get_players(data["Home"]),
        )

        self.away = Team(
            data["GuestEmpty"],
            data["Guest"],
            data["Set" + str(self.current_set) + "Guest"],
            data["WonSetGuest"],
            self._get_players(data["Guest"]),
        )
        self.stats.initiate(data, self.current_set)
        self.status = data["Status"]
        self._reset_stream()
        self._update_ui()
        self._get_logos()

    def _get_players(self, team_id):
        """Get the list of players of the team"""
        data_rq = {
            "data": '{"H":"signalrlivehubfederations","M":"getRosterData","A":["'
            + str(self.m_id)
            + '",'
            + str(team_id)
            + ',"'
            + self.league
            + '"]}',
        }
        data = self._web_request(data_rq)
        players = {}
        for player in data:
            players[str(player["N"])] = player["NM"] + " " + player["SR"]
        return players

    def _set_point(self):
        self.set_point = False
        self.match_point = False
        if self.current_set == 5:
            if self.home.points >= 14 and self.home.points - self.away.points >= 2:
                self.match_point = True
            elif self.away.points >= 14 and self.away.points - self.home.points >= 2:
                self.match_point = True
            else:
                self.match_point = False
        elif self.home.sets >= 2 or self.away.sets >= 2:
            if self.home.sets >= 2 and self.home.points >= 24 and self.home.points - self.away.points >= 1:
                self.match_point = True
            elif self.away.sets >= 2 and self.away.points >= 24 and self.away.points - self.home.points >= 1:
                self.match_point = True
            elif self.home.sets >= 2 and self.away.points >= 24 and self.away.points - self.home.points >= 1:
                self.set_point = True
            if self.away.sets >= 2 and self.home.points >= 24 and self.home.points - self.away.points >= 1:
                self.set_point = True
            else:
                self.match_point = False
                self.set_point = False
        else:
            if self.home.points >= 24 and self.home.points - self.away.points >= 2:
                self.set_point = True
            elif self.away.points >= 24 and self.away.points - self.home.points >= 2:
                self.set_point = True
            else:
                self.set_point = False

        self.streamer.set_point(self.set_point)
        self.streamer.match_point(self.match_point)

    def _update_ui(self):
        if self.status == 0:
            self.window["-ID-"].update(disabled=False)
            self.window["-ERROR-"].update(
                "No ha comenzado", text_color="yellow", visible=True
            )
            self.window["-HOME-"].update(visible=False)
            self.window["-AWAY-"].update(visible=False)
            self.window["-ST-"].update("Parar", disabled=False)
        elif self.status == 1:
            self.window["-ID-"].update(disabled=True)
            self.window["-ERROR-"].update(visible=False)
            self.window["-HOME-"].update(visible=True)
            self.window["-AWAY-"].update(visible=True)
            self.window["-ST-"].update("Parar", disabled=False)
        elif self.status == 2:
            self.window["-ID-"].update(disabled=False)
            self.window["-ERROR-"].update(
                "Ya terminó", text_color="yellow", visible=True
            )
            self.window["-HOME-"].update(visible=False)
            self.window["-AWAY-"].update(visible=False)
            self.window["-ST-"].update("Iniciar", disabled=False)
        self.window["-HOME-"].update(
            value=self.home.name + " - "+ str(self.home.sets)+ " | " + str(self.home.points), visible=True
        )
        self.window["-AWAY-"].update(
            value= str(self.away.points) + " | " + str(self.away.sets) + " - " + self.away.name, visible=True
        )

    def _make_statistics(self):
        try:
            self.stats.update(self.home.points, self.away.points, self.current_set)
        except:
            pass

    def _get_logos(self):
        """Gets the logos of the teams in the match"""
        homeurl="https://images.dataproject.com/livosur/TeamLogo/512/512/TeamLogo_{}.jpg".format(self.home.id)
        awayurl="https://images.dataproject.com/livosur/TeamLogo/512/512/TeamLogo_{}.jpg".format(self.away.id)
        self.streamer._set_input_settings(self.elements["HOME_LOGO"], {"file": homeurl})
        self.streamer._set_input_settings(self.elements["AWAY_LOGO"], {"file": awayurl})

    def _web_request(self, data):
        """makes the requests to the server with the specified data"""
        cookies = {
            "ARRAffinitySameSite": "02acb1319a69edaf85b38e14f86a1d4a24942007f49c27a9216d162dc8017f28",
        }
        headers = {
            "Accept": "text/plain, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": self.league_url,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-GPC": "1",
        }
        params = {
            "transport": "serverSentEvents",
            "clientProtocol": self.credentials["ProtocolVersion"],
            "connectionToken": self.credentials["ConnectionToken"],
            "connectionData": '[{"name":"signalrlivehubfederations"}]',
        }
        return requests.post(
            "https://dataprojectservicesignalradv.azurewebsites.net/signalr/send",
            params=params,
            cookies=cookies,
            headers=headers,
            data=data,
        ).json()["R"]

    def _get_credentials(self):
        """Gets the credentials needed for the requests"""
        headers = {
            "Accept": "text/plain, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.6",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": self.league_url,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Sec-GPC": "1",
        }

        params = {
            "clientProtocol": "1.5",
            "connectionData": '[{"name":"signalrlivehubfederations"}]',
        }

        response = requests.get(
            "https://dataprojectservicesignalradv.azurewebsites.net/signalr/negotiate",
            params=params,
            headers=headers,
        ).json()
        self.credentials = response

    def _update_stream(self):
        try:
            self.streamer._set_input_settings(
                self.elements["HOME_NAME"], {"text": self.home.name}
            )
            self.streamer._set_input_settings(
                self.elements["AWAY_NAME"], {"text": self.away.name}
            )
            self.streamer._set_input_settings(
                self.elements["HOME_POINTS"], {"text": str(self.home.points)}
            )
            self.streamer._set_input_settings(
                self.elements["AWAY_POINTS"], {"text": str(self.away.points)}
            )
            self.streamer._set_input_settings(
                self.elements["HOME_SET"], {"text": str(self.home.sets)}
            )
            self.streamer._set_input_settings(
                self.elements["AWAY_SET"], {"text": str(self.away.sets)}
            )
            self.streamer._set_input_settings(
                self.elements["HOME_STATS_PT"],
                {"text": str(self.stats.total["Home_percentage"])},
            )
            self.streamer._set_input_settings(
                self.elements["AWAY_STATS_PT"],
                {"text": str(self.stats.total["Away_percentage"])},
            )
            self.streamer._set_input_settings(
                self.elements["HOME_STATS_PuntosT"],
                {"text": str(self.stats.total["Home_points"])},
            )
            self.streamer._set_input_settings(
                self.elements["AWAY_STATS_PuntosT"],
                {"text": str(self.stats.total["Away_points"])},
            )
            for x in self.stats.sets.keys():
                print(x)
                self.streamer._set_input_settings(
                    self.elements["HOME_STATS_P" + str(x.split("_")[1])],
                    {"text": str(self.stats.sets[x]["Home_percentage"])},
                )
                self.streamer._set_input_settings(
                    self.elements["AWAY_STATS_P" + str(x.split("_")[1])],
                    {"text": str(self.stats.sets[x]["Away_percentage"])},
                )
                self.streamer._set_input_settings(
                    self.elements["HOME_STATS_S" + str(x.split("_")[1])],
                    {"text": str(self.stats.sets[x]["Home_points"])},
                )
                self.streamer._set_input_settings(
                    self.elements["AWAY_STATS_S" + str(x.split("_")[1])],
                    {"text": str(self.stats.sets[x]["Away_points"])},
                )
        except Exception as e:
            print("error", e)
            return e
        
    def _reset_stream(self):
        try:
            self.streamer._set_input_settings(
                self.elements["HOME_NAME"], {"text": ""}
            )
            self.streamer._set_input_settings(
                self.elements["AWAY_NAME"], {"text": ""}
            )
            self.streamer._set_input_settings(
                self.elements["HOME_POINTS"], {"text": ""}
            )
            self.streamer._set_input_settings(
                self.elements["AWAY_POINTS"], {"text": ""}
            )
            self.streamer._set_input_settings(
                self.elements["HOME_SET"], {"text": ""}
            )
            self.streamer._set_input_settings(
                self.elements["AWAY_SET"], {"text": ""}
            )
            self.streamer._set_input_settings(
                self.elements["HOME_STATS_PT"], {"text": ""},
            )
            self.streamer._set_input_settings(
                self.elements["AWAY_STATS_PT"], {"text": ""},
            )
            self.streamer._set_input_settings(
                self.elements["HOME_STATS_PuntosT"], {"text": ""},
            )
            self.streamer._set_input_settings(
                self.elements["AWAY_STATS_PuntosT"], {"text": ""},
            )
            for x in range(1,6):
                self.streamer._set_input_settings(
                    self.elements["HOME_STATS_P" + str(x)],
                    {"text": ""},
                )
                self.streamer._set_input_settings(
                    self.elements["AWAY_STATS_P" + str(x)],
                    {"text": ""},
                )
                self.streamer._set_input_settings(
                    self.elements["HOME_STATS_S" + str(x)],
                    {"text": ""},
                )
                self.streamer._set_input_settings(
                    self.elements["AWAY_STATS_S" + str(x)],
                    {"text": ""},
                )
            self.streamer._set_input_settings(self.elements["HOME_LOGO"], {"file": ""})
            self.streamer._set_input_settings(self.elements["AWAY_LOGO"], {"file": ""})
        except Exception as e:
            print("error", e)
            return e

    def _stop(self):
        self.is_running = False
        self.status = 2
        self._reset_stream()
        self._update_ui()


# Match(5953,'livosur')
