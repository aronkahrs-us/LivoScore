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
        self._get_inputs()
        pass

    def test(self):
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "http://192.168.68.107:8088",
            "Referer": "http://192.168.68.107:8088/titles/?key=a9188c6c-5852-4e7f-a478-717432399c3f",
            "Sec-GPC": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        }

        params = {
            "key": "a9188c6c-5852-4e7f-a478-717432399c3f",
        }

        data = {
            "txtHome Name.Text": "HOME",
            "txtAway Name.Text": "123",
            "txtHome Set.Text": "0",
            "txtAway Set.Text": "1",
            "txtHome Score.Text": "0",
            "txtAway Score.Text": "0",
            "Update": "Update",
        }

        response = requests.post(
            "http://192.168.68.107:8088/titles/",
            params=params,
            headers=headers,
            data=data,
            verify=False,
        )

    def _set_active(self,index,input):
        self._set_input('OverlayInput{}In'.format(index),input)

    def _set_inactive(self,index,input):
        self._set_input('OverlayInput{}Out'.format(index),input)

    def _set_image(self,input,name,value):
        self._set_input('SetImage',input,name,value)
    
    def _set_text(self,input,name,value):
        self._set_input('SetText',input,name,value)

    def _set_input(self,function=None,input=None,name=None,value=None):
        req = requests.post('http://{}:{}/API/?Function={}&Input={}&SelectedName={}&Value={}'.format(self.connect['IP'],self.connect['PORT'],function,input,name,value))
        print(req)

    def _get_inputs(self):
        self.inputs={}
        req = requests.get("http://{}:{}/api".format(self.connect['IP'],self.connect['PORT'])).content
        inputs_xlm = xmltodict.parse(req)["vmix"]["inputs"]["input"]
        for x in inputs_xlm:
            data = {
                'key':x['@key'],
                'type':x['@type'],
                'title':x['@title'],
                'state':x['@state'],
                'key':x['@key'],
            }
            if x['@type'] == 'GT':
                try:
                    data['text']=(x['text'])
                except:
                    pass
                try:
                    data['image']=(x['image'])
                except:
                    pass
            self.inputs[x['@shortTitle']] = data
        print(self.inputs)
        pass


hand=Vmix()
# hand._set_active(1,hand.inputs['scoreboard']['key'])
# hand._set_active(2,hand.inputs['Substitution']['key'])
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