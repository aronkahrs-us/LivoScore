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
        except:
            pass
        try:
            with open("./Config/elem_config.json", "r") as openfile:
                # Reading from json file
                self.elements = json.load(openfile)
        except:
            pass
        self._get_inputs()
        pass

    def test_connection(self):
        try:
            response = requests.get("http://{}:{}/api".format(self.connect['IP'],self.connect['PORT']), timeout=5)
            if response.ok:
                return 'OK'
            else:
                return 'ERROR'
        except requests.exceptions.Timeout:
            return "ERROR"
    
    def test_connection_params(self, ip, port, passw=None) -> str:
        try:
            response = requests.get("http://{}:{}/api".format(ip,port), timeout=5)
            if response.ok:
                return 'OK'
            else:
                return 'ERROR'
        except requests.exceptions.Timeout:
            return "ERROR"
 
    def serve(self,team):
        if team == '*':
            self._set_inactive(1,self.elements['A_SERVE']['key'])
            self._set_active(1,self.elements['H_SERVE']['key'])
        elif team == 'a':
            self._set_inactive(1,self.elements['H_SERVE']['key'])
            self._set_active(1,self.elements['A_SERVE']['key'])
    
    def substitution(self,team):
        if team == '*':
            self._set_image(self.elements['H_SUBSTITUTION']['key'],self.elements['H_SUBSTITUTION']['image'][0]['@name'],'https://images.dataproject.com/livosur/TeamLogo/512/512/TeamLogo_501.jpg')
            self._set_active(2,self.elements['H_SUBSTITUTION']['key'])
        elif team == 'a':
            self._set_image(self.elements['A_SUBSTITUTION']['key'],self.elements['A_SUBSTITUTION']['image'][0]['@name'],'https://images.dataproject.com/livosur/TeamLogo/512/512/TeamLogo_505.jpg')
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
    
    def _set_active(self,index,input):
        self._set_input('OverlayInput{}In'.format(index),input)

    def _set_inactive(self,index,input):
        self._set_input('OverlayInput{}Out'.format(index),input)

    def _set_input_settings(self,input,value):
        self._set_input(input=input['parent'],name=input['name'],value=value)

    def _set_input(self,function=None,input=None,name=None,value:dict=None):
        if function == None:
            function = 'SetText' if 'text' in value else 'SetImage'
            value = value['text'] if 'text' in value else value['file']
        req = requests.post('http://{}:{}/API/?Function={}&Input={}&SelectedName={}&Value={}'.format(self.connect['IP'],self.connect['PORT'],function,input,name,value))

    def _get_inputs(self):
        self.inputs={}
        req = requests.get("http://{}:{}/api".format(self.connect['IP'],self.connect['PORT'])).content
        inputs_xlm = xmltodict.parse(req)["vmix"]["inputs"]["input"]
        for x in inputs_xlm:
            data = {
                'key':x['@key'],
                'type':x['@type'],
                'name':x['@title'],
                'state':x['@state'],
            }
            if x['@type'] == 'GT':
                try:
                    data['text']=(x['text'])
                    for k in x['text']:
                        self.inputs[k['@name']] = {
                            'name': k['@name'],
                            'parent': x['@key'],
                        }
                except:
                    pass
                try:
                    data['image']=(x['image'])
                    for k in x['image']:
                        self.inputs[k['@name']] = {
                            'name': k['@name'],
                            'parent': x['@key'],
                        }
                except:
                    pass
            self.inputs[x['@shortTitle']] = data
        # for x in self.inputs:
        #     print(x,self.inputs[x])
        return self.inputs

# try:
#     with open("./Config/elem_config.json", "r") as openfile:
#         # Reading from json file
#         elements = json.load(openfile)
# except:
#     pass
# hand=Vmix()
# homeurl="https://images.dataproject.com/livosur/TeamLogo/512/512/TeamLogo_{}.jpg".format(505)
# awayurl="https://images.dataproject.com/livosur/TeamLogo/512/512/TeamLogo_{}.jpg".format(501)
# hand._set_input_settings(elements["HOME_NAME"], {"text": ''})
# hand._set_input_settings(elements["HOME_LOGO"], {"file": ''})
# hand._set_input_settings(elements["AWAY_NAME"], {"text": ''})
# hand._set_input_settings(elements["AWAY_LOGO"], {"file": ''})
# hand._set_active(1,hand.inputs['scoreboard']['key'])
# hand._set_active(2,hand.inputs['Substitution']['key'])
# hand.set_point(True)
# time.sleep(2)
# hand._set_inactive(2,hand.inputs['Substitution']['key'])
# hand.set_image(hand.inputs['scoreboard']['key'],hand.inputs['scoreboard']['image'][0]['@name'],'https://images.dataproject.com/livosur/TeamLogo/512/512/TeamLogo_501.jpg')
# hand.set_image(hand.inputs['scoreboard']['key'],hand.inputs['scoreboard']['image'][1]['@name'],'https://images.dataproject.com/livosur/TeamLogo/512/512/TeamLogo_505.jpg')
# hand.set_text(hand.inputs['scoreboard']['key'],hand.inputs['scoreboard']['text'][0]['@name'],'Nacional')
# hand.set_text(hand.inputs['scoreboard']['key'],hand.inputs['scoreboard']['text'][1]['@name'],'Sanjo')
# hand.set_text(hand.inputs['scoreboard']['key'],hand.inputs['scoreboard']['text'][2]['@name'],'1')
# hand.set_text(hand.inputs['scoreboard']['key'],hand.inputs['scoreboard']['text'][3]['@name'],'1')
# hand.set_text(hand.inputs['scoreboard']['key'],hand.inputs['scoreboard']['text'][4]['@name'],'1')
# hand.set_text(hand.inputs['scoreboard']['key'],hand.inputs['scoreboard']['text'][5]['@name'],'1')
# time.sleep(5)
# hand.set_image(hand.inputs['scoreboard']['key'],hand.inputs['scoreboard']['image'][0]['@name'],'')
# hand.set_image(hand.inputs['scoreboard']['key'],hand.inputs['scoreboard']['image'][1]['@name'],'')
# hand.set_text(hand.inputs['scoreboard']['key'],hand.inputs['scoreboard']['text'][0]['@name'],'')
# hand.set_text(hand.inputs['scoreboard']['key'],hand.inputs['scoreboard']['text'][1]['@name'],'')
# hand.set_text(hand.inputs['scoreboard']['key'],hand.inputs['scoreboard']['text'][2]['@name'],'')
# hand.set_text(hand.inputs['scoreboard']['key'],hand.inputs['scoreboard']['text'][3]['@name'],'')
# hand.set_text(hand.inputs['scoreboard']['key'],hand.inputs['scoreboard']['text'][4]['@name'],'')
# hand.set_text(hand.inputs['scoreboard']['key'],hand.inputs['scoreboard']['text'][5]['@name'],'')