import requests
import time
import json
import os
import shutil
import threading
from Utils.obs import obs
import wget
from bs4 import BeautifulSoup
from sseclient import SSEClient

class Match:
    def __init__(self,m_id,window):
        self.m_id=int(m_id)
        self.is_running = True
        self.obsApi = obs()
        self.set_point = False
        self.match_point = False
        self.window=window
        self.stats = {}
        try:
            with open('./Config/api_config.json', 'r') as openfile:
                # Reading from json file
                config = json.load(openfile)
                self.league = config['LEAGUE']
                self.league_url = config['LEAGUE_URL']
        except:
            self.league = ""
        try:
            with open('./Config/elem_config.json', 'r') as openfile:
                # Reading from json file
                self.elements = json.load(openfile)
        except:
            self.elements = {}
        self._get_credentials()
        self.cookies = {
        'ARRAffinitySameSite': 'd4cf45d89d11a6d9b07a5dbd364ea4432ecfd8782dd6765a42a25cf772133186',
        }
        self.headers = {
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': self.league_url,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
        }
        self.negotiate()
        threading.Thread(target=self.connect).start()
        #self.connect()

    def negotiate(self):

        params = {
            'clientProtocol': '1.5',
            'connectionData': '[{"name":"signalrlivehubfederations"}]',
            '_': str(round(time.time() * 1000)),
        }

        response = requests.get(
            'https://dataprojectservicesignalr.azurewebsites.net/signalr/negotiate',
            params=params,
            cookies=self.cookies,
            headers=self.headers,
        ).json()
        self.token= response['ConnectionToken']

    def connect(self):
        headers = {
            'Accept': 'text/event-stream',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Origin': self.league_url,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
        }

        params = {
            'transport': 'serverSentEvents',
            'clientProtocol': '1.5',
            'connectionToken': self.token,
            'connectionData': '[{"name":"signalrlivehubfederations"}]',
            'tid': '1',
        }

        # Create an SSE clients
        messages = SSEClient(
        'https://dataprojectservicesignalr.azurewebsites.net/signalr/connect',
        params=params,
        cookies=self.cookies,
        headers=headers,
        )
        self.start()
        self.send()
        # Iterate through SSE events
        x=0
        for msg in messages:
            if self.is_running == False:
                print('STOP')
                break
            try:
                data=msg.data.replace("'","\"")
                if data != 'initialized' and data != '{}':
                    data = json.loads(data)
                    try:
                        print('___________')
                        print(data["M"][0]["M"])
                        if data["M"][0]["M"] == "refreshPlayByPlayData":
                            self.rally=data["M"][0]["A"][0][-1]
                            self.serve=data["M"][0]["A"][0][-1]['Team']
                            self.action=data["M"][0]["A"][0][-1]['RallyT']
                            self.skill=data["M"][0]["A"][0][-1]['Skill']
                            if self.action == 0 or self.action == 1:
                                threading.Thread(target=self.obsApi.serve,args=self.serve).start()
                            elif self.action == 2:
                                threading.Thread(target=self.obsApi.substitution, args=self.serve).start()
                            elif self.action == 3:
                                threading.Thread(target=self.obsApi.time_out).start()
                        elif data["M"][0]["M"] == "updateMatchSetData_ES" or data["M"][0]["M"] == "updateMatchSetData_DV":
                            self.current_set=data["M"][0]["A"][0]['SN']
                            self.home['Points']=data["M"][0]["A"][0]['HP']
                            self.away['Points']=data["M"][0]["A"][0]['GP']
                        elif data["M"][0]["M"] == "updateMatchScoreData_ES" or data["M"][0]["M"] == "updateMatchScoreData_DV":
                            self.home['Sets']=data["M"][0]["A"][0]['H']
                            self.away['Sets']=data["M"][0]["A"][0]['G']
                            self.status=data["M"][0]["A"][0]["S"]
                    finally:
                        if self.status == 2:
                            self._stop()
                        threading.Thread(target=self._set_point).start()
                        threading.Thread(target=self._update_stream).start()
                        threading.Thread(target=self._update_ui).start()
                        x=x+1
                        if x == 15:
                            threading.Thread(target=self._make_statistics).start()
                            x=0
                            
            except Exception as e:
                print(e)
                pass
        self._delete_files()

    def start(self):
        params = {
            'transport': 'serverSentEvents',
            'clientProtocol': '1.5',
            'connectionToken': self.token,
            'connectionData': '[{"name":"signalrlivehubfederations"}]',
            '_': str(round(time.time() * 1000)),
        }

        response = requests.get(
            'https://dataprojectservicesignalr.azurewebsites.net/signalr/start',
            params=params,
            cookies=self.cookies,
            headers=self.headers,
        ).json()
        print(response)

    def send(self):
        params = {
            'transport': 'serverSentEvents',
            'clientProtocol': '1.5',
            'connectionToken': self.token,
            'connectionData': '[{"name":"signalrlivehubfederations"}]',
        }

        data = {
            'data': '{"H":"signalrlivehubfederations","M":"getLiveScoreListData_From_ES","A":["'+str(self.m_id)+'","'+self.league+'"],"I":0}',
        }

        data = requests.post(
            'https://dataprojectservicesignalr.azurewebsites.net/signalr/send',
            params=params,
            cookies=self.cookies,
            headers=self.headers,
            data=data,
        ).json()['R'][0]
        print(data)
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
        self.status = data['Status']
        self._update_stream()
        self._update_ui()
        self._get_logos()

    def _get_players(self, team_id):
        """Get the list of players of the team"""
        data_rq = {
            'data': '{"H":"signalrlivehubfederations","M":"getRosterData","A":["'+str(self.m_id)+'",'+str(team_id)+',"'+self.league+'"]}',
        }
        data = self._web_request(data_rq)
        players = {}
        for player in data:
            players[str(player['N'])] = player['NM']+' '+player['SR']
        return players

    def _set_point(self):
        self.set_point = False
        self.match_point = False
        if self.current_set == 5:
            if self.home['Points'] >= 14 and self.home['Points'] - self.away['Points'] >= 2:
                self.match_point = True
            elif self.away['Points'] >= 14 and self.away['Points'] - self.home['Points'] >= 2:
                self.match_point = True
            else:
                self.match_point = False
        elif self.home['Sets'] >= 2 or self.away['Sets'] >= 2:
            if self.home['Points'] >= 24 and self.home['Points'] - self.away['Points'] >= 2:
                self.match_point = True
            elif self.away['Points'] >= 24 and self.away['Points'] - self.home['Points'] >= 2:
                self.match_point = True
            else:
                self.match_point = False
        else:
            if self.home['Points'] >= 24 and self.home['Points'] - self.away['Points'] >= 2:
                self.set_point = True
            elif self.away['Points'] >= 24 and self.away['Points'] - self.home['Points'] >= 2:
                self.set_point = True
            else:
                self.set_point = False
        
        self.obsApi.set_point(self.set_point)
        self.obsApi.match_point(self.match_point)

    def _update_ui(self):
        if self.status==0:
            self.window['-ID-'].update(disabled=False)
            self.window['-ERROR-'].update("No ha comenzado", text_color='yellow', visible=True)
            self.window['-HOME-'].update(visible=False)
            self.window['-AWAY-'].update(visible=False)
            self.window['-ST-'].update('Parar',disabled=False)
        elif self.status==1:
            self.window['-ID-'].update(disabled=True)
            self.window['-ERROR-'].update(visible=False)
            self.window['-HOME-'].update(visible=True)
            self.window['-AWAY-'].update(visible=True)
            self.window['-ST-'].update('Parar',disabled=False)
        elif self.status==2:
            self.window['-ID-'].update(disabled=False)
            self.window['-ERROR-'].update("Ya terminó", text_color='yellow', visible=True)
            self.window['-HOME-'].update(visible=False)
            self.window['-AWAY-'].update(visible=False)
            self.window['-ST-'].update('Iniciar',disabled=False)
        self.window['-HOME-'].update(value=self.home['Name'] +
                                ' - ' + str(self.home['Points']), visible=True)
        self.window['-AWAY-'].update(value=self.away['Name'] +
                                ' - ' + str(self.away['Points']), visible=True)
    
    def _test_make_statistics(self):
        set_total_points = self.home['Points'] + self.away['Points']
        self.stats['Set_'+str(self.current_set)] = {
            "Total_points": set_total_points,
            "Home_points": self.home['Points'],
            "Away_points": self.away['Points'],
            "Home_percentage": round((self.home['Points']*100)/set_total_points),
            "Away_percentage": round((self.away['Points']*100)/set_total_points),
        }
        for x in self.stats.keys():
            if x != 'Total':
                data=self.stats[x]
                self.stats['Total']['Total_points'] += data['Total_points']
                self.stats['Total']['Home_points'] += data['Home_points']
                self.stats['Total']['Away_points'] += data['Away_points']
        self.stats['Total']['Home_percentage'] = round((self.stats['Total']['Home_points']*100)/self.stats['Total']['Total_points'])
        self.stats['Total']['Away_percentage'] = round((self.stats['Total']['Away_points']*100)/self.stats['Total']['Total_points'])

    def _make_statistics(self):
        """makes all the stats of the match"""
        data_rq = {
            'data': '{"H":"signalrlivehubfederations","M":"getLiveScoreData_From_DV","A":["'+str(self.m_id)+'","'+self.league+'"],"I":0}',
        }

        data = self._web_request(data_rq)
        percents = []
        Home_tot_points = 0
        Away_tot_points = 0
        for i in range(1, 6):
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
            Home_points_percent = round((Home_tot_points*100) / \
                (Home_tot_points+Away_tot_points))
            Away_points_percent = round((Away_tot_points*100) / \
                (Home_tot_points+Away_tot_points))
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
        try:
            files = {
                'Home_points_percent_s1': percents[0],
                'Away_points_percent_s1': percents[1],
                'Home_points_percent_s2': percents[2],
                'Away_points_percent_s2': percents[3],
                'Home_points_percent_s3': percents[4],
                'Away_points_percent_s3': percents[5],
                'Home_points_percent_s4': percents[6],
                'Away_points_percent_s4': percents[7],
                'Home_points_percent_s5': percents[8],
                'Away_points_percent_s5': percents[9],
                'Home_points_percent': Home_points_percent,
                'Away_points_percent': Away_points_percent,
                'Home_points_s1': data['Set1Home'],
                'Away_points_s1': data['Set1Guest'],
                'Home_points_s2': data['Set2Home'],
                'Away_points_s2': data['Set2Guest'],
                'Home_points_s3': data['Set3Home'],
                'Away_points_s3': data['Set3Guest'],
                'Home_points_s4': data['Set4Home'],
                'Away_points_s4': data['Set4Guest'],
                'Home_points_s5': data['Set5Home'],
                'Away_points_s5': data['Set5Guest'],
                'Home_points': Home_tot_points,
                'Away_points': Away_tot_points,
            }
            for file, value in files.items():
                path = os.path.join(os.getcwd(), r'stats')
                if not os.path.exists(path):
                    os.makedirs(path)
                fw = open('./stats/'+file+'.txt', 'w')
                fw.write(str(value))
                fw.close()
        except:
            pass

    def _get_logos(self):
        """Gets the logos of the teams in the match"""
        URL = str(self.league_url)+"/LiveScore_adv.aspx?ID="+str(self.m_id)
        r = requests.get(URL, verify=True)

        soup = BeautifulSoup(r.content, 'html5lib')

        home = soup.find('div', attrs={'id': 'DIV_LogoHome_Image'})['style']
        homeurl = home.strip('background-image:url(').strip(');')
        away = soup.find('div', attrs={'id': 'DIV_LogoGuest_Image'})['style']
        awayurl = away.strip('background-image:url(').strip(');')
        wget.download(homeurl, "home.jpg")
        wget.download(awayurl, "away.jpg")
    
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

    def _update_stream(self):
        try:
            self.obsApi._set_input_settings(self.elements['HOME_NAME'],{'text': self.home['Name']})
            self.obsApi._set_input_settings(self.elements['AWAY_NAME'],{'text': self.away['Name']})
            self.obsApi._set_input_settings(self.elements['HOME_POINTS'],{'text': str(self.home['Points'])})
            self.obsApi._set_input_settings(self.elements['AWAY_POINTS'],{'text': str(self.away['Points'])})
            self.obsApi._set_input_settings(self.elements['HOME_SET'],{'text': str(self.home['Sets'])})
            self.obsApi._set_input_settings(self.elements['AWAY_SET'],{'text': str(self.away['Sets'])})
        except Exception as e:
            print(e)
            return e



    def _create_files(self):
        files = {
                'Home': self.home['Name'],
                'Home_id': self.home['Id'],
                'Home_points': self.home['Points'],
                'Home_sets': self.home['Sets'],
                'Away': self.away['Name'],
                'Away_id': self.away['Id'],
                'Away_points': self.away['Points'],
                'Away_sets': self.away['Sets'],
                'Current_set': self.current_set,
                }
        for file, value in files.items():
            fw = open(file+'.txt', 'w')
            fw.write(str(value))
            fw.close()
    
    def _delete_files(self):
        files = [
            'Home',
            'Away']
        for file in files:
            try:
                os.remove(file+".jpg")
            except:
                continue
        shutil.rmtree('stats')

    def _stop(self) -> bool:
        self.is_running=False
        self.status=2
        self._delete_files()
        self._update_ui()


#EvSt(5953,'livosur')._update_stream()

#Livosur().get_ready_matches()