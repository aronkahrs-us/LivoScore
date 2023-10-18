import requests
import json
import ssl
from datetime import datetime, timezone
from bs4 import BeautifulSoup


class League:
    def __init__(self) -> None:
        ssl._create_default_https_context = ssl._create_unverified_context
        try:
            with open("./Config/league_config.json", "r") as openfile:
                # Reading from json file
                config = json.load(openfile)
                self.league = config["LEAGUE"]
                self.league_url = config["LEAGUE_URL"]
        except:
            self.league = ""
        self._get_credentials()
        pass

    def get_ready_matches(self) -> dict:
        if int(datetime.now(tz=timezone.utc).strftime("%d")) == int(datetime.now().strftime("%d")):
            matches = {}
            URL = str(self.league_url) + "/MainLiveScore.aspx"
            r = requests.get(URL, verify=True)
            soup = BeautifulSoup(r.content, "lxml")
            try:
                id = soup.find("input", {"id": "HF_MatchesList"}).get("value")
                id = id.split(";")
                for x in id:
                    Home = soup.find(
                        "span", {"id": "Content_Main_RLV_MatchList_Label1_" + str(x)}
                    ).text
                    Guest = soup.find(
                        "span", {"id": "Content_Main_RLV_MatchList_Label2_" + str(x)}
                    ).text
                    status = soup.find(
                        "div", {"id": "Content_Main_RLV_MatchList_DIV_FinalResult_" + str(x)}
                    ).get("style")
                    if status == None:
                        matches[int(x)] = str(str(Home) + " vs " + str(Guest))
                json_object = json.dumps(matches, indent=4)
                with open("./Config/matches.json", "w") as outfile:
                    outfile.write(json_object)
            except Exception as e:
                print("Got unhandled exception %s" % str(e))
            return matches
        else:
            try:
                with open("./Config/matches.json", "r") as openfile:
                    # Reading from json file
                    matches = json.load(openfile)
                    return matches
            except:
                self.matches = {}

    def _get_data(self, id):
        """Gets the status of the match(not started, ongoing or ended)"""
        data_rq = {
            "data": '{"H":"signalrlivehubfederations","M":"getLiveScoreData_From_DV","A":["'
            + str(id)
            + '","'
            + self.league
            + '"],"I":0}',
        }
        return self._web_request(data_rq)

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


League().get_ready_matches()