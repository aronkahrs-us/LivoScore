import requests
import json

class Player:
    def __init__(self, m_id, t_id, p_id) -> None:
        self.m_id = m_id
        self.t_id=t_id
        self.id = p_id
        try:
            with open("./Config/league_config.json", "r") as openfile:
                # Reading from json file
                config = json.load(openfile)
                self.league = config["LEAGUE"]
                self.league_url = config["LEAGUE_URL"]
        except Exception as e:
            print(f"AN EXCEPTION OCCURRED!", e)
        self._get_credentials()
        self._get_data()
        pass

    def _get_data(self):
        data_rq = {
            "data": '{"H":"signalRLiveHubFederations","M":"getPlayerStatisticsData","A":["'+str(self.m_id)+'",'+str(self.t_id)+',"'+self.league+'"],"I":5}',
        }
        data = self._web_request(data_rq)
        for x in data:
            if x['PID']==self.id:
                print(x)
        test=[x for x in data if x['PID'] == self.id][0]
        print(test)

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

Player(4588,407,6071)