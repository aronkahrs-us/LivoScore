import requests
import xmltodict
import json
import time

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

    def test_connection(self):
        try:
            response = self.session.get("http://{}:{}/api".format(self.connect['IP'],self.connect['PORT']), timeout=5)
            if response.ok:
                return 'OK'
            else:
                return 'ERROR'
        except requests.exceptions.Timeout:
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
        except requests.exceptions.Timeout:
            return "ERROR"
 
    def serve(self,team):
        self.l_team
        if self.l_team != team:
            if team == '*':
                self._set_inactive(1,self.elements['A_SERVE']['key'])
                self._set_active(1,self.elements['H_SERVE']['key'])
            elif team == 'a':
                self._set_inactive(1,self.elements['H_SERVE']['key'])
                self._set_active(1,self.elements['A_SERVE']['key'])
        self.l_team=team
    
    def substitution(self,team,h_id,a_id):
        if team == '*':
            self._set_input(input=self.elements['H_SUBSTITUTION']['key'],name=self.elements['H_SUBSTITUTION']['image'][0]['@name'],value={'file':'https://images.dataproject.com/livosur/TeamLogo/512/512/TeamLogo_{}.jpg'.format(h_id)})
            self._set_active(2,self.elements['H_SUBSTITUTION']['key'])
        elif team == 'a':
            self._set_input(input=self.elements['A_SUBSTITUTION']['key'],name=self.elements['A_SUBSTITUTION']['image'][0]['@name'],value={'file':'https://images.dataproject.com/livosur/TeamLogo/512/512/TeamLogo_{}.jpg'.format(a_id)})
            self._set_active(2,self.elements['A_SUBSTITUTION']['key'])
        time.sleep(5)
        self._set_inactive(2,self.elements['A_SUBSTITUTION']['key'])

    def time_out(self):
        self._set_active(2,self.elements['TIME_OUT']['key'])
        time.sleep(60)
        self._set_inactive(2,self.elements['TIME_OUT']['key'])

    def match_point(self, show:bool):
        if show:
            self._set_active(3,self.elements['MATCH_POINT']['key'])
        else:
            self._set_inactive(3,self.elements['MATCH_POINT']['key'])

    def set_point(self, show:bool):
        if show:
            self._set_active(3,self.elements['SET_POINT']['key'])
        else:
            self._set_inactive(3,self.elements['SET_POINT']['key'])
    
    def update_logos(self,home:str=None,away:str=None):
        for x in self.inputs:
            if ('home' in x.lower() or 'h' in x.lower()) and 'logo' in x.lower():
                self._set_input_settings(self.inputs[x],{'file': home})
            elif ('away' in x.lower() or 'a' in x.lower()) and 'logo' in x.lower():
                self._set_input_settings(self.inputs[x],{'file': away})

    def update_referees(self,names:list):
        for x in self.elements['REFEREES']['text']:
            self._set_input_settings(self.inputs[x['@name']],{'text': names[-1]})
            names.pop(-1)
            if len(names) == 0:
                break

    def set_sp_stat(self,home,away):
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

    def set_results(self,home,away):
        #HOME
        self._set_input(input=self.elements['RESULTS_H']['key'],name=self.elements['RESULTS_H']['text'][0]['@name'],value={'text': str(home['result_03'])})
        self._set_input(input=self.elements['RESULTS_H']['key'],name=self.elements['RESULTS_H']['text'][1]['@name'],value={'text': str(home['result_13'])})
        self._set_input(input=self.elements['RESULTS_H']['key'],name=self.elements['RESULTS_H']['text'][2]['@name'],value={'text': str(home['result_23'])})
        self._set_input(input=self.elements['RESULTS_H']['key'],name=self.elements['RESULTS_H']['text'][3]['@name'],value={'text': str(home['result_32'])})
        self._set_input(input=self.elements['RESULTS_H']['key'],name=self.elements['RESULTS_H']['text'][4]['@name'],value={'text': str(home['result_31'])})
        self._set_input(input=self.elements['RESULTS_H']['key'],name=self.elements['RESULTS_H']['text'][5]['@name'],value={'text': str(home['result_30'])})
        #AWAY
        self._set_input(input=self.elements['RESULTS_A']['key'],name=self.elements['RESULTS_A']['text'][0]['@name'],value={'text': str(away['result_03'])})
        self._set_input(input=self.elements['RESULTS_A']['key'],name=self.elements['RESULTS_A']['text'][1]['@name'],value={'text': str(away['result_13'])})
        self._set_input(input=self.elements['RESULTS_A']['key'],name=self.elements['RESULTS_A']['text'][2]['@name'],value={'text': str(away['result_23'])})
        self._set_input(input=self.elements['RESULTS_A']['key'],name=self.elements['RESULTS_A']['text'][3]['@name'],value={'text': str(away['result_32'])})
        self._set_input(input=self.elements['RESULTS_A']['key'],name=self.elements['RESULTS_A']['text'][4]['@name'],value={'text': str(away['result_31'])})
        self._set_input(input=self.elements['RESULTS_A']['key'],name=self.elements['RESULTS_A']['text'][5]['@name'],value={'text': str(away['result_30'])})

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
        req = self.session.post('http://{}:{}/API/?Function={}&Input={}&SelectedName={}&Value={}'.format(self.connect['IP'],self.connect['PORT'],function,input,name,value))
    
    def _get_inputs(self):
        self.inputs={}
        req = self.session.get("http://{}:{}/api".format(self.connect['IP'],self.connect['PORT'])).content
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

    def _add_input(self,value,name):
        req = self.session.post('http://{}:{}/API/?Function=AddInput&Value={}&SelectedName={}'.format(self.connect['IP'],self.connect['PORT'],value,name))