import requests
import json

class test:
    def __init__(self,m_id) -> None:
        self.id =m_id
        try:
            with open("./Config/league_config.json", "r") as openfile:
                # Reading from json file
                config = json.load(openfile)
                self.league = config["LEAGUE"]
                self.league_url = config["LEAGUE_URL"]
        except Exception as e:
            print(f"AN EXCEPTION OCCURRED!", e)
        self._get_credentials()
        pass

    def getLUD(self):
        data_rq = {
            "data": '{"H":"signalrlivehubfederations","M":"getLineUpData","A":["'+ str(self.id)+ '","'+ self.league+ '"]}',
        }
        data = self._web_request(data_rq)
        print(data)

    def getLSI_DV(self):
        data_rq = {
            "data": '{"H":"signalrlivehubfederations","M":"getLiveScore_Init_Data_From_DV","A":["'+ str(self.id)+ '","'+ self.league+ '"]}',
        }
        data = self._web_request(data_rq)
        for x in data:
            print(x,': ',data[x])
            print('_______')

    def getRD(self,team):
        data_rq = {
            "data": '{"H":"signalrlivehubfederations","M":"getRosterData","A":["'+ str(self.id)+ '","'+ str(team)+ '","'+ self.league+ '"]}',
        }
        data = self._web_request(data_rq)
        print(data)

    def getPSD(self,team):
        data_rq = {
            "data": '{"H":"signalrlivehubfederations","M":"getPlayerStatisticsData","A":["'+ str(self.id)+ '","'+ str(team)+ '","'+ self.league+ '"]}',
        }
        data = self._web_request(data_rq)
        print(data)

    def join(self):
        data_rq = {
            "data": '{"H":"signalRLiveHubBetting","M":"joinGroup"]}',
        }
        data = self._web_request(data_rq)
        print(data)
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

test(5996).join()