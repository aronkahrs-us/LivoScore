import requests
import xmltodict
import json
import time
import urllib3.exceptions as urlexp

class Vmix:
    def __init__(self) -> None:
        try:
            with open("./Config/stream_config.json", "r") as openfile:
                # Reading from json file
                self.connect = json.load(openfile)
                self.session = requests.Session()
                self.session.auth = ('admin', self.connect['PASS']) 
        except:
            pass
        try:
            with open("./Config/elem_config.json", "r") as openfile:
                # Reading from json file
                self.elements = json.load(openfile)
        except:
            pass
        self.l_team =''
        self._get_inputs()

    def test_connection(self) -> str:
        try:
            response = self.session.get("http://{}:{}/api".format(self.connect['IP'],self.connect['PORT']), timeout=5)
            if response.ok:
                return 'OK'
            else:
                return 'ERROR'
        except:
            return "ERROR"
    
    def test_connection_params(self, ip, port, passw=None) -> str:
        try:
            session = requests.Session()
            session.auth = ('admin', passw) 
            response = session.get("http://{}:{}/api".format(ip,port), timeout=5)
            if response.ok:
                return 'OK'
            else:
                return 'ERROR'
        except:
            return "ERROR"
 
    def serve(self,team):
        try:
            self.l_team
            if self.l_team != team:
                if team == '*':
                    self._set_inactive(1,self.elements['A_SERVE']['key'])
                    self._set_active(1,self.elements['H_SERVE']['key'])
                elif team == 'a':
                    self._set_inactive(1,self.elements['H_SERVE']['key'])
                    self._set_active(1,self.elements['A_SERVE']['key'])
            self.l_team=team
        except Exception as e:
            print('serve',e)
    
    def substitution(self,team,home,away):
        try:
            if team == '*':
                self._set_input(input=self.elements['H_SUBSTITUTION']['key'],name=self.elements['H_SUBSTITUTION']['image']['@name'],value={'file':home})
                self._set_active(2,self.elements['H_SUBSTITUTION']['key'])
            elif team == 'a':
                self._set_input(input=self.elements['A_SUBSTITUTION']['key'],name=self.elements['A_SUBSTITUTION']['image']['@name'],value={'file':away})
                self._set_active(2,self.elements['A_SUBSTITUTION']['key'])
            time.sleep(5)
            self._set_inactive(2,self.elements['A_SUBSTITUTION']['key'])
        except Exception as e:
            print('substitution',e)

    def time_out(self):
        try:
            if self.elements['AUTOMATE_TIME_OUT']:
                self._set_active(2,self.elements['TIME_OUT']['key'])
                time.sleep(60)
                self._set_inactive(2,self.elements['TIME_OUT']['key'])
        except Exception as e:
            print('time_out',e)

    def match_point(self, show:bool):
        try:
            if show:
                self._set_active(3,self.elements['MATCH_POINT']['key'])
            else:
                self._set_inactive(3,self.elements['MATCH_POINT']['key'])
        except Exception as e:
            print('match_point',e)

    def set_point(self, show:bool):
        try:
            if show:
                self._set_active(3,self.elements['SET_POINT']['key'])
            else:
                self._set_inactive(3,self.elements['SET_POINT']['key'])
        except Exception as e:
            print('set_point',e)
    
    def update_logos(self,home:str=None,away:str=None):
        try:
            for x in self.inputs:
                if 'home' in x.lower() and 'logo' in x.lower():
                    self._set_input_settings(self.inputs[x],{'file': home})
                elif 'away' in x.lower() and 'logo' in x.lower():
                    self._set_input_settings(self.inputs[x],{'file': away})
        except Exception as e:
            print('update_logos',e)

    def update_names(self,home:str=None,away:str=None):
        try:
            for x in self.inputs:
                if ('home' in x.lower()) and 'name' in x.lower():
                    self._set_input_settings(self.inputs[x],{'text': home})
                elif ('away' in x.lower()) and 'name' in x.lower():
                    self._set_input_settings(self.inputs[x],{'text': away})
        except Exception as e:
            print('update_names',e)
    
    def update_players(self,team:str=None,players=None,clear:bool=False):
        """ Method to update players list, for home use team as H and for away use team as A"""
        try:
            player_tk=''
            if clear:
                for i in range(1,19):
                    self._set_input_settings(self.inputs['H PlyNum{}.Text'.format(i)],{'text': '0'})
                    self._set_input_settings(self.inputs['H PlyN{}.Text'.format(i)],{'text': 'Nombre Apellido'})
                    self._set_input_settings(self.inputs['A PlyNum{}.Text'.format(i)],{'text': '0'})
                    self._set_input_settings(self.inputs['A PlyN{}.Text'.format(i)],{'text': 'Nombre Apellido'})
                self._set_input_settings(self.inputs['TK Players H.Text'],{'text': '1 - Nombre Apellido 2 - Nombre Apellido 3 - Nombre Apellido '})
                self._set_input_settings(self.inputs['TK Players A.Text'],{'text': '1 - Nombre Apellido 2 - Nombre Apellido 3 - Nombre Apellido '})
            else:
                i=1
                for player in players:
                    self._set_input_settings(self.inputs['{} PlyNum{}.Text'.format(team.upper(),i)],{'text': player.number})
                    self._set_input_settings(self.inputs['{} PlyN{}.Text'.format(team.upper(),i)],{'text': player.name})
                    player_tk += str(player.number) + ' - ' + player.name + ' '
                    i+=1
                if i <18:
                    for j in range(i,19):
                        self._set_input_settings(self.inputs['{} PlyNum{}.Text'.format(team.upper(),j)],{'text': ''})
                        self._set_input_settings(self.inputs['{} PlyN{}.Text'.format(team.upper(),j)],{'text': ''})
                self._set_input_settings(self.inputs['TK Players {}.Text'.format(team.capitalize())],{'text': player_tk})
        except Exception as e:
            print('update_players',e)
    
    def update_coaches(self,team:str=None,coach:str=None,clear:bool=False):
        """ Method to update coaches"""
        try:
            if clear:
                self._set_input_settings(self.inputs['CH Home DT.Text'],{'text': 'Nombre Apellido'})
                self._set_input_settings(self.inputs['CH Away DT.Text'],{'text': 'Nombre Apellido'})
            else:
                self._set_input_settings(self.inputs['CH {} DT.Text'.format(team)],{'text': coach})
        except Exception as e:
            print('update_coaches',e)

    def update_winner(self,team=None,clear=None):
        try:
            if clear:
                self._set_input(input=self.elements['WINNER']['key'],name=self.elements['WINNER']['text']['@name'],value={'text': ''})
                self._set_input(input=self.elements['WINNER']['key'],name=self.elements['WINNER']['image']['@name'],value={'file': ''})
            else:
                if self.elements['IS_FINAL']:
                    text = team.name+ " CAMPEON!!"
                else:
                    text = team.name+ " GANÓ!!"
                self._set_input(input=self.elements['WINNER']['key'],name=self.elements['WINNER']['text']['@name'],value={'text': text})
                self._set_input(input=self.elements['WINNER']['key'],name=self.elements['WINNER']['image']['@name'],value={'file': team.logo})
        except Exception as e:
            print('update_winner',e)
    
    def update_match_history(self,total=None,home=None,away=None,clear=None):
        try:
            if clear:
                self._set_input(input=self.elements['MATCH_HISTORY']['key'],
                                name=[value['@name'] for value in self.elements['MATCH_HISTORY']['text'] if 'total matches' in value['@name'].lower()][0],
                                value={'text': 'NN'})
                self._set_input(input=self.elements['MATCH_HISTORY']['key'],
                                name=[value['@name'] for value in self.elements['MATCH_HISTORY']['text'] if 'won home' in value['@name'].lower()][0],
                                value={'text': 'NN'})
                self._set_input(input=self.elements['MATCH_HISTORY']['key'],
                                name=[value['@name'] for value in self.elements['MATCH_HISTORY']['text'] if 'won away' in value['@name'].lower()][0],
                                value={'text': 'NN'})
            else:
                self._set_input(input=self.elements['MATCH_HISTORY']['key'],
                                name=[value['@name'] for value in self.elements['MATCH_HISTORY']['text'] if 'total matches' in value['@name'].lower()][0],
                                value={'text': total})
                self._set_input(input=self.elements['MATCH_HISTORY']['key'],
                                name=[value['@name'] for value in self.elements['MATCH_HISTORY']['text'] if 'won home' in value['@name'].lower()][0],
                                value={'text': home})
                self._set_input(input=self.elements['MATCH_HISTORY']['key'],
                                name=[value['@name'] for value in self.elements['MATCH_HISTORY']['text'] if 'won away' in value['@name'].lower()][0],
                                value={'text': away})
                #self._set_input(input=self.elements['MATCH_HISTORY']['key'],name=self.elements['MATCH_HISTORY']['image']['@name'],value={'file': team.logo})
        except Exception as e:
            print('update_match_history',e)

    def update_referees(self,names:list):
        try:
            for x in self.elements['REFEREES']['text']:
                self._set_input_settings(self.inputs[x['@name']],{'text': names[-1]})
                names.pop(-1)
                if len(names) == 0:
                    break
        except Exception as e:
            print('update_referees',e)

    def set_sp_stat(self,home,away):
        try:
            #HOME
            self._set_input(input=self.elements['SP_STAT_H']['key'],name=self.elements['SP_STAT_H']['text'][0]['@name'],value={'text': 'Sets Ganados'})
            self._set_input(input=self.elements['SP_STAT_H']['key'],name=self.elements['SP_STAT_H']['text'][1]['@name'],value={'text': str(home['set_percent'])+'%'})
            self._set_input(input=self.elements['PP_STAT_H']['key'],name=self.elements['PP_STAT_H']['text'][0]['@name'],value={'text': 'Puntos Ganados'})
            self._set_input(input=self.elements['PP_STAT_H']['key'],name=self.elements['PP_STAT_H']['text'][1]['@name'],value={'text': str(home['points_percent'])+'%'})
            #AWAY
            self._set_input(input=self.elements['SP_STAT_A']['key'],name=self.elements['SP_STAT_A']['text'][0]['@name'],value={'text': 'Sets Ganados'})
            self._set_input(input=self.elements['SP_STAT_A']['key'],name=self.elements['SP_STAT_A']['text'][1]['@name'],value={'text': str(away['set_percent'])+'%'})
            self._set_input(input=self.elements['PP_STAT_A']['key'],name=self.elements['PP_STAT_A']['text'][0]['@name'],value={'text': 'Puntos Ganados'})
            self._set_input(input=self.elements['PP_STAT_A']['key'],name=self.elements['PP_STAT_A']['text'][1]['@name'],value={'text': str(away['points_percent'])+'%'})
        except Exception as e:
            print('set_sp_stat',e)

    def set_results(self,home=None,away=None, clear:bool=None):
        rs= ['result_03','result_13','result_23','result_32','result_31','result_30']
        try:
            if clear:
                for i in range(0,6):
                    #HOME
                    self._set_input(input=self.elements['RESULTS_H']['key'],name=self.elements['RESULTS_H']['text'][i]['@name'],value={'text': '0'})
                    #AWAY
                    self._set_input(input=self.elements['RESULTS_A']['key'],name=self.elements['RESULTS_A']['text'][i]['@name'],value={'text': '0'})
            else:
                for i in range(0,6):
                    #HOME
                    self._set_input(input=self.elements['RESULTS_H']['key'],name=self.elements['RESULTS_H']['text'][i]['@name'],value={'text': str(home[rs[i]])})
                    #AWAY
                    self._set_input(input=self.elements['RESULTS_A']['key'],name=self.elements['RESULTS_A']['text'][i]['@name'],value={'text': str(away[rs[i]])})
        except Exception as e:
            print('set_results',e)

    def _set_active(self,index,input):
        self._set_input('OverlayInput{}In'.format(index),input)

    def _set_inactive(self,index,input):
        self._set_input('OverlayInput{}Out'.format(index),input)

    def _set_input_settings(self,input,value):
        self._set_input(input=input['parent'],name=input['name'].replace('_1',''),value=value)

    def _set_input(self,function=None,input=None,name=None,value:dict=None):
        if function == None:
            function = 'SetText' if 'text' in value else 'SetImage'
            value = value['text'] if 'text' in value else value['file']
        self.session.post('http://{}:{}/API/?Function={}&Input={}&SelectedName={}&Value={}'.format(self.connect['IP'],self.connect['PORT'],function,input,name,value),timeout=5)
    
    def _get_inputs(self) -> dict:
        self.inputs={}
        try:
            req = self.session.get("http://{}:{}/api".format(self.connect['IP'],self.connect['PORT']),timeout=5).content
            inputs_xlm = xmltodict.parse(req)["vmix"]["inputs"]["input"]
            for x in inputs_xlm:
                data = {
                    'key':x['@key'],
                    'type':x['@type'],
                    'name':x['@title'],
                }
                if x['@type'] == 'GT':
                    try:
                        data['text']=(x['text'])
                        for k in x['text']:
                            self.inputs[k['@name']] = {
                                'name': k['@name'],
                                'parent': x['@key'],
                            }
                    except Exception as e:
                        pass
                    try:
                        data['image']=(x['image'])
                        if type(x['image']) == list:
                            for k in x['image']:
                                self.inputs[k['@name']] = {
                                    'name': k['@name'],
                                    'parent': x['@key'],
                                }
                        else:
                            k=x['image']
                            if k['@name'] in self.inputs:
                                k['@name']=k['@name']+'_1'
                            self.inputs[k['@name']] = {
                                    'name': k['@name'],
                                    'parent': x['@key'],
                                }
                    except Exception as e:
                        pass
                self.inputs[x['@shortTitle']] = data
            # for x in self.inputs:
            #    print(x)
            #    print(self.inputs[x])
            #    print('____')
            return dict(sorted(self.inputs.items()))
        except requests.exceptions.ConnectionError as e:
            self.inputs = {}

    def _add_input(self,value,name):
        self.session.post('http://{}:{}/API/?Function=AddInput&Value={}&SelectedName={}'.format(self.connect['IP'],self.connect['PORT'],value,name))

v=Vmix()
v.update_match_history(clear=True)