import requests
import wget
from bs4 import BeautifulSoup, SoupStrainer
import requests
import json
import ssl

class livosur:
    def __init__(self) -> None:
        ssl._create_default_https_context = ssl._create_unverified_context
        try:
            with open('api_config.json', 'r') as openfile:
                # Reading from json file
                config = json.load(openfile)
                self.league = config['LEAGUE']
                self.league_url = config['LEAGUE_URL']
        except:
            self.league = ""
        self._get_credentials()
        pass

    def get_ready_matches(self) -> dict:
        matches = {}
        URL = str(self.league_url)+"/MainLiveScore.aspx"
        r = requests.get(URL, verify=True)
        soup = BeautifulSoup(r.content, 'lxml')
        try: 
            id = soup.find('input', {'id': 'HF_MatchesList'}).get('value')
            id = id.split(';')
            for x in id:
                Home = soup.find('span', {'id': 'Content_Main_RLV_MatchList_Label1_'+str(x)}).text
                Guest = soup.find('span', {'id': 'Content_Main_RLV_MatchList_Label2_'+str(x)}).text
                matches[int(x)]=str(str(Home)+' vs '+str(Guest))
        except Exception as e:
            print("Got unhandled exception %s" % str(e))
        return matches

    def _get_data(self,id):
        """Gets the status of the match(not started, ongoing or ended)"""
        data_rq = {
            'data': '{"H":"signalrlivehubfederations","M":"getLiveScoreData_From_DV","A":["'+str(id)+'","'+self.league+'"],"I":0}',
        }
        return self._web_request(data_rq)
    
    def _web_request(self, data):
        """makes the requests to the server with the specified data"""
        cookies = {
            'ARRAffinitySameSite': '02acb1319a69edaf85b38e14f86a1d4a24942007f49c27a9216d162dc8017f28',
        }
        headers = {
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': self.league_url,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-GPC': '1',
        }
        params = {
            'transport': 'serverSentEvents',
            'clientProtocol': self.credentials['ProtocolVersion'],
            'connectionToken': self.credentials['ConnectionToken'],
            'connectionData': '[{"name":"signalrlivehubfederations"}]',
        }
        return requests.post('https://dataprojectservicesignalradv.azurewebsites.net/signalr/send',
                             params=params, cookies=cookies, headers=headers, data=data).json()['R']

    def _get_credentials(self):
        """Gets the credentials needed for the requests"""
        headers = {
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': self.league_url,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-GPC': '1',
        }

        params = {
            'clientProtocol': '1.5',
            'connectionData': '[{"name":"signalrlivehubfederations"}]',
        }

        response = requests.get(
            'https://dataprojectservicesignalradv.azurewebsites.net/signalr/negotiate',
            params=params,
            headers=headers,
        ).json()
        self.credentials = response


class match:

    def __init__(self, id:int):
        """constructor of the class"""
        ssl._create_default_https_context = ssl._create_unverified_context
        self.id = id
        try:
            with open('api_config.json', 'r') as openfile:
                # Reading from json file
                config = json.load(openfile)
                self.league = config['LEAGUE']
                self.league_url = config['LEAGUE_URL']
        except:
            self.league = ""

        self._get_credentials()
        #self._get_logos()
        self._updater()

    def _get_credentials(self):
        """Gets the credentials needed for the requests"""
        headers = {
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.6',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': self.league_url,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-GPC': '1',
        }

        params = {
            'clientProtocol': '1.5',
            'connectionData': '[{"name":"signalrlivehubfederations"}]',
        }

        response = requests.get(
            'https://dataprojectservicesignalradv.azurewebsites.net/signalr/negotiate',
            params=params,
            headers=headers,
        ).json()
        self.credentials = response

    def _get_data(self):
        """Gets the data of the match and the teams"""
        data_rq = {
            'data': '{"H":"signalrlivehubfederations","M":"getLiveScoreData_From_DV","A":["'+str(self.id)+'","'+self.league+'"],"I":0}',
        }
        data = self._web_request(data_rq)
        self.current_set = data['WonSetHome'] + data['WonSetGuest'] + 1
        if self.current_set > 5:
            self.current_set = 5
        self.home = {
            'Name': data['HomeEmpty'],
            'Id': data['Home'],
            'Points': data['Set'+str(self.current_set)+'Home'],
            'Sets': data['WonSetHome'],
            'Players': self._get_players(data['Home'])
        }
        self.away = {
            'Name': data['GuestEmpty'],
            'Id': data['Guest'],
            'Points': data['Set'+str(self.current_set)+'Guest'],
            'Sets': data['WonSetGuest'],
            'Players': self._get_players(data['Guest'])
        }
        ###############################################
        # Esto manda la data a los archivos que usa OBS
        # pero todavia no se como voy a manejar eso y no
        # se si quiero que la clase haga todo de una
        # o hacerlo separado
        ###############################################
        # files = {
        #     'Home': data['HomeEmpty'],
        #     'Home_id': data['Home'],
        #     'Home_points': data['Set'+str(current_set)+'Home'],
        #     'Home_sets': data['WonSetHome'],
        #     'Away': data['GuestEmpty'],
        #     'Away_id': data['Guest'],
        #     'Away_points': data['Set'+str(current_set)+'Guest'],
        #     'Away_sets': data['WonSetGuest'],
        #     'Current_set': current_set,
        # }
        # for file, value in files.items():
        #     fw = open(file+'.txt', 'w')
        #     fw.write(str(value))
        #     fw.close()

    def _get_status(self):
        """Gets the status of the match(not started, ongoing or ended)"""
        data_rq = {
            'data': '{"H":"signalrlivehubfederations","M":"getLiveScoreData_From_DV","A":["'+str(self.id)+'","'+self.league+'"],"I":0}',
        }
        self.status = self._web_request(data_rq)['Status']

    def _get_logos(self):
        """Gets the logos of the teams in the match"""
        URL = str(self.league_url)+"/LiveScore_adv.aspx?ID="+str(self.id)
        r = requests.get(URL, verify=True)

        soup = BeautifulSoup(r.content, 'html5lib')

        home = soup.find('div', attrs={'id': 'DIV_LogoHome_Image'})['style']
        homeurl = home.strip('background-image:url(').strip(');')
        away = soup.find('div', attrs={'id': 'DIV_LogoGuest_Image'})['style']
        awayurl = away.strip('background-image:url(').strip(');')
        wget.download(homeurl, "home.jpg")
        wget.download(awayurl, "away.jpg")

    def _get_players(self, team_id):
        """Get the list of players of the team"""
        data_rq = {
            'data': '{"H":"signalrlivehubfederations","M":"getRosterData","A":["'+str(self.id)+'",'+str(team_id)+',"'+self.league+'"]}',
        }
        data = self._web_request(data_rq)
        players = {}
        for player in data:
            players[str(player['N'])] = player['NM']+' '+player['SR']
        return players
        ###############################################
        # Esto manda la data a los archivos que usa OBS
        # pero todavia no se como voy a manejar eso y no
        # se si quiero que la clase haga todo de una
        # o hacerlo separado
        ###############################################
        # fw = open(team+'_team.json', 'w')
        # fw.write(json.dumps(players, indent=4))
        # fw.close()

    def _make_statistics(self):
        """makes all the stats of the match"""
        data_rq = {
            'data': '{"H":"signalrlivehubfederations","M":"getLiveScoreData_From_DV","A":["'+str(self.id)+'","'+self.league+'"],"I":0}',
        }

        data = self._web_request(data_rq)
        percents = []
        for i in range(1, self.current_set+1):
            try:
                Home_points_percent = str(round(
                    (data['Set'+str(i)+'Home']*100)/(data['Set'+str(i)+'Home']+data['Set'+str(i)+'Guest'])))+' %'
                Away_points_percent = str(round((data['Set'+str(i)+'Guest']*100)/(
                    data['Set'+str(i)+'Home']+data['Set'+str(i)+'Guest'])))+' %'
            except ZeroDivisionError:
                Home_points_percent = 0
                Away_points_percent = 0
            percents.append(Home_points_percent)
            percents.append(Away_points_percent)
        try:
            Home_tot_points = data['Set1Home']+data['Set2Home'] + \
                data['Set3Home']+data['Set4Home']+data['Set5Home']
            Away_tot_points = data['Set1Guest']+data['Set2Guest'] + \
                data['Set3Guest']+data['Set4Guest']+data['Set5Guest']
            Home_points_percent = (Home_tot_points*100) / \
                (Home_tot_points+Away_tot_points)
            Away_points_percent = (Away_tot_points*100) / \
                (Home_tot_points+Away_tot_points)
        except ZeroDivisionError:
            Home_tot_points = 0
            Away_tot_points = 0
            Home_points_percent = 0
            Away_points_percent = 0
        ###############################################
        # Esto manda la data a los archivos que usa OBS
        # pero todavia no se como voy a manejar eso y no
        # se si quiero que la clase haga todo de una
        # o hacerlo separado
        ###############################################
        # files = {
        #     'Home_points_percent_s1': percents[0],
        #     'Away_points_percent_s1': percents[1],
        #     'Home_points_percent_s2': percents[2],
        #     'Away_points_percent_s2': percents[3],
        #     'Home_points_percent_s3': percents[4],
        #     'Away_points_percent_s3': percents[5],
        #     'Home_points_percent_s4': percents[6],
        #     'Away_points_percent_s4': percents[7],
        #     'Home_points_percent_s5': percents[8],
        #     'Away_points_percent_s5': percents[9],
        #     'Home_points_percent': Home_points_percent,
        #     'Away_points_percent': Away_points_percent,
        #     'Home_points_s1': data['Set1Home'],
        #     'Away_points_s1': data['Set1Guest'],
        #     'Home_points_s2': data['Set2Home'],
        #     'Away_points_s2': data['Set2Guest'],
        #     'Home_points_s3': data['Set3Home'],
        #     'Away_points_s3': data['Set3Guest'],
        #     'Home_points_s4': data['Set4Home'],
        #     'Away_points_s4': data['Set4Guest'],
        #     'Home_points_s5': data['Set5Home'],
        #     'Away_points_s5': data['Set5Guest'],
        #     'Home_points': Home_tot_points,
        #     'Away_points': Away_tot_points,
        # }
        # for file, value in files.items():
        #     path = os.path.join(os.getcwd(), r'stats')
        #     if not os.path.exists(path):
        #         os.makedirs(path)
        #     fw = open('./stats/'+file+'.txt', 'w')
        #     fw.write(str(value))
        #     fw.close()
        # return files

    def _rally(self):
        try:
            data_rq = {
                'data': '{"H":"signalrlivehubfederations","M":"getPlayByPlayData","A":["' + str(self.id) + '",' + str(self.current_set-1) + ',"'+self.league+'",false]}'}
            response = self._web_request(data_rq)
            response = response[len(response)-1]
            self.team_serve = 'Home' if response['ST'] else 'Away'
            rally = response['RallyT']
            if rally == 3:
                self.to = True
            if rally == 2:
                if rally['Team'] == 'a':
                    self.last_substitution = 'Away'
                if rally['Team'] == '*':
                    self.last_substitution = 'Home'
        finally:
            pass

    def _set_point(self):
        if self.current_set == 5:
            if self.home['Points'] >= 14 and self.home['Points'] - self.away['Points'] >= 2:
                self.match_point = True
            elif self.away['Points'] >= 14 and self.away['Points'] - self.home['Points'] >= 2:
                self.match_point = True
            else:
                self.match_point = False
        elif (5-self.away['Sets'])-self.home['Sets'] >= 2 or (5-self.home['Sets'])-self.away['Sets'] >= 2:
            if self.home['Points'] >= 14 and self.home['Points'] - self.away['Points'] >= 2:
                self.match_point = True
            elif self.away['Points'] >= 14 and self.away['Points'] - self.home['Points'] >= 2:
                self.match_point = True
            else:
                self.match_point = False
        else:
            if self.home['Points'] >= 24 and self.home['Points'] - self.away['Points'] >= 2:
                self.set_point = True
            elif self.away['Points'] >= 4 and self.away['Points'] - self.home['Points'] >= 2:
                self.set_point = True
            else:
                self.set_point = False

    def _updater(self):
        self._get_data()
        self._get_status()
        self._rally()
        self._set_point()
        self._make_statistics()

    def _web_request(self, data):
        """makes the requests to the server with the specified data"""
        cookies = {
            'ARRAffinitySameSite': '02acb1319a69edaf85b38e14f86a1d4a24942007f49c27a9216d162dc8017f28',
        }
        headers = {
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.7',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': self.league_url,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-GPC': '1',
        }
        params = {
            'transport': 'serverSentEvents',
            'clientProtocol': self.credentials['ProtocolVersion'],
            'connectionToken': self.credentials['ConnectionToken'],
            'connectionData': '[{"name":"signalrlivehubfederations"}]',
        }
        return requests.post('https://dataprojectservicesignalradv.azurewebsites.net/signalr/send',
                             params=params, cookies=cookies, headers=headers, data=data).json()['R']


#test= livosur().get_ready_matches()
# test_m = match(test)
# print(test.__dict__)
# print('__________________')
# print(test.home['Name'])
# print('------------------')