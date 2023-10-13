import requests
import wget
from bs4 import BeautifulSoup
import requests
import os
import json
import shutil
import ssl
from datetime import datetime
from obs import Obs
import html

ssl._create_default_https_context = ssl._create_unverified_context
obsApi = Obs()
def get_league():
    try:
        with open('api_config.json', 'r') as openfile:
            # Reading from json file
            config = json.load(openfile)
            global league_name
            league_name = config['LEAGUE']
            return config['LEAGUE_URL']
    except:
        return ""
    
def get_credentials():
    headers = {
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': get_league(),
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
    return response
cookies = {
    'ARRAffinitySameSite': '02acb1319a69edaf85b38e14f86a1d4a24942007f49c27a9216d162dc8017f28',
}

headers = {
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.7',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': get_league(),
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-GPC': '1',
}

params = {
    'transport': 'serverSentEvents',
    'clientProtocol': get_credentials()['ProtocolVersion'],
    'connectionToken': get_credentials()['ConnectionToken'],
    'connectionData': '[{"name":"signalrlivehubfederations"}]',
}


def get_data(id):
    data_rq = {
        'data': '{"H":"signalrlivehubfederations","M":"getLiveScoreData_From_DV","A":["'+str(id)+'","'+league_name+'"],"I":0}',
    }
    data = requests.post('https://dataprojectservicesignalradv.azurewebsites.net/signalr/send',
                         params=params, cookies=cookies, headers=headers, data=data_rq).json()['R']
    current_set = data['WonSetHome'] + data['WonSetGuest'] + 1
    if current_set > 5:
        current_set = 5
    files = {
        'Home': data['HomeEmpty'],
        'Home_id': data['Home'],
        'Home_points': data['Set'+str(current_set)+'Home'],
        'Home_sets': data['WonSetHome'],
        'Away': data['GuestEmpty'],
        'Away_id': data['Guest'],
        'Away_points': data['Set'+str(current_set)+'Guest'],
        'Away_sets': data['WonSetGuest'],
        'Current_set': current_set,
    }
    for file, value in files.items():
        fw = open(file+'.txt', 'w')
        fw.write(str(value))
        fw.close()
    return files

def get_status(id):
    data_rq = {
        'data': '{"H":"signalrlivehubfederations","M":"getLiveScoreData_From_DV","A":["'+str(id)+'","'+league_name+'"],"I":0}',
    }

    data = requests.post('https://dataprojectservicesignalradv.azurewebsites.net/signalr/send',
                         params=params, cookies=cookies, headers=headers, data=data_rq).json()['R']['Status']
    return data

def get_logos(id):
    URL = str(get_league())+"/LiveScore_adv.aspx?ID="+str(id)
    print(URL)
    r = requests.get(URL, verify=False)

    soup = BeautifulSoup(r.content, 'html5lib')

    home = soup.find('div', attrs={'id': 'DIV_LogoHome_Image'})['style']
    homeurl = home.strip('background-image:url(').strip(');')
    away = soup.find('div', attrs={'id': 'DIV_LogoGuest_Image'})['style']
    awayurl = away.strip('background-image:url(').strip(');')
    wget.download(homeurl, "home.jpg")
    wget.download(awayurl, "away.jpg")

def get_team(id, team_id, team):
    data_rq = {
        'data': '{"H":"signalrlivehubfederations","M":"getRosterData","A":["'+str(id)+'",'+str(team_id)+',"'+league_name+'"]}',
    }

    data = requests.post('https://dataprojectservicesignalradv.azurewebsites.net/signalr/send',
                         params=params, cookies=cookies, headers=headers, data=data_rq).json()['R']
    # print(data)
    players = {}
    for player in data:
        players[str(player['N'])] = player['NM']+' '+player['SR']
    fw = open(team+'_team.json', 'w')
    fw.write(json.dumps(players, indent=4))
    fw.close()

def statistics(id):
    data_rq = {
        'data': '{"H":"signalrlivehubfederations","M":"getLiveScoreData_From_DV","A":["'+str(id)+'","'+league_name+'"],"I":0}',
    }

    data = requests.post('https://dataprojectservicesignalradv.azurewebsites.net/signalr/send',
                         params=params, cookies=cookies, headers=headers, data=data_rq).json()['R']
    percents = []
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
        Home_points_percent = (Home_tot_points*100) / \
            (Home_tot_points+Away_tot_points)
        Away_points_percent = (Away_tot_points*100) / \
            (Home_tot_points+Away_tot_points)
    except ZeroDivisionError:
        Home_tot_points = 0
        Away_tot_points = 0
        Home_points_percent = 0
        Away_points_percent = 0
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
    return files

def serve(id, current_set):
    try:
        data_rq = {
            'data': '{"H":"signalrlivehubfederations","M":"getPlayByPlayData","A":["' + str(id) + '",' + str(current_set) + ',"'+league_name+'",false]}'}
        data = requests.post('https://dataprojectservicesignalradv.azurewebsites.net/signalr/send',
                             params=params, cookies=cookies, headers=headers, data=data_rq).json()['R']
        data = data[len(data) - 1]['ST']
        return data
    finally:
        pass

def time_out(id, current_set):
    try:
        data_rq = {
            'data': '{"H":"signalrlivehubfederations","M":"getPlayByPlayData","A":["' + str(id) + '",' + str(current_set) + ',"'+league_name+'",false]}'}
        data = requests.post('https://dataprojectservicesignalradv.azurewebsites.net/signalr/send',
                             params=params, cookies=cookies, headers=headers, data=data_rq).json()['R']
        print(data)
        data = data[len(data) - 1]['RallyT']
        if data == 3: 
            return True
    finally:
        pass

def substitution(id, current_set):

    try:
        data_rq = {
            'data': '{"H":"signalrlivehubfederations","M":"getPlayByPlayData","A":["' + str(id) + '",' + str(current_set) + ',"'+league_name+'",false]}'}
        data = requests.post('https://dataprojectservicesignalradv.azurewebsites.net/signalr/send',
                             params=params, cookies=cookies, headers=headers, data=data_rq).json()['R']
        data = data[len(data) - 1]['RallyT']
        print("SUB:",data)
        if data == 2:
            if data['Team'] == 'a':
                return 'Away'
            if data['Team'] == '*':
                return 'Home'
    finally:
        pass

def set_point(home, away, home_set, away_set, current_set):
    if current_set == 5:
        if home == 14 and away < 14:
            obsApi.match_point('show')
        elif home < 14 and away == 14:
            obsApi.match_point('show')
        elif home >= 14 and away >= 14:
            if home == away + 1:
                obsApi.match_point('show')
            if away == home + 1:
                obsApi.match_point('show')
    elif home == 24 and away < 24:
        if home_set == 2 and away_set < 2:
            obsApi.match_point('show')
        else:
            obsApi.set_point('show')
    elif home < 24 and away == 24:
        if home_set < 2 and away_set == 2:
            obsApi.match_point('show')
        else:
            obsApi.set_point('show')
    elif home >= 24 and away >= 24:
        if home == away + 1:
            if home_set == 2 and away_set < 2:
                obsApi.match_point('show')
            else:
                obsApi.set_point('show')
        if away == home + 1:
            if home_set < 2 and away_set == 2:
                obsApi.match_point('show')
            else:
                obsApi.set_point('show')
    else:
        obsApi.match_point('hide')
        obsApi.set_point('hide')

def delete():
    files = [
        'Home',
        'Home_sets',
        'Home_points',
        'Home_id',
        'Home_serve',
        'Away',
        'Away_sets',
        'Away_points',
        'Away_id',
        'Away_serve',
        'Current_set']
    for file in files:
        try:
            os.remove(file+".txt")
            if file == 'Home' or file == "Away":
                os.remove(file+".jpg")
                os.remove(file+"_team.json")
            shutil.rmtree('stats')
        except:
            continue

def get_matches(start,len):
    matches = {}
    for i in range(start,start+len+1):
        data_rq = {
            'data': '{"H":"signalrlivehubfederations","M":"getLiveScoreData_From_DV","A":["'+str(i)+'","'+league_name+'"],"I":0}',
        }
        data = requests.post('https://dataprojectservicesignalradv.azurewebsites.net/signalr/send',
                            params=params, cookies=cookies, headers=headers, data=data_rq).json()['R']
        print(data)
        if data['Status'] != 2 and data['HomeEmpty'] != None:
            matches[data['ChampionshipMatchID']]=str(data['HomeEmpty']+' - '+data['GuestEmpty'])
    print(matches,league_name)
    return matches

# def test_get_matchs(cat):
#     """Gets the logos of the teams in the match"""
#     URL = "https://livosur-web.dataproject.com/CompetitionHome.aspx?ID="+str(cat)
#     r = requests.get(URL, verify=False)

#     soup = BeautifulSoup(r.content, 'html5lib')

#     home = soup.find('div', attrs={'id': 'RT_LastTodayNext_Matches'}).find(class_="rrRelativeWrapper").find(class_="rrClipRegion").find(class_="rrItemsList").find_all('li')
#     print(home)

# def test_web():
#     data_rq = {
#         'data': '{"H":"signalRLiveHub","M":"getLiveScore_Init_Data_From_DV","A":["5851","livosur"],"I":0}',
#     }

#     data = requests.post('https://dataprojectservicesignalradv.azurewebsites.net/signalr/send',
#                          params=params, cookies=cookies, headers=headers, data=data_rq).text
#     print(html.unescape(data))
#     return data
    

