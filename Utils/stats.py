import requests 
from bs4 import BeautifulSoup

class TeamStats:
    def __init__(self,l_url) -> None:
        self.total = {
            "Total_points": 0,
            "Home_points": 0,
            "Away_points": 0,
            "Home_percentage": "0",
            "Away_percentage": "0",
        }
        self.league_url=l_url
        self.sets = {}
        pass

    def initiate(self, data, current_set):
        try:
            self._match_history(data['ChampionshipMatchID'],data['Home'],data['Guest'])
        except:
            pass
        sets = ["Set{}Home", "Set{}Guest"]
        for i in range(1, current_set + 1):
            try:
                set_total_points = data[sets[0].format(i)] + data[sets[1].format(i)]
                self.sets["Set_" + str(i)] = {
                    "Total_points": set_total_points,
                    "Home_points": data[sets[0].format(i)],
                    "Away_points": data[sets[1].format(i)],
                    "Home_percentage": str(
                        round((data[sets[0].format(i)] * 100) / set_total_points)
                    )
                    + "%",
                    "Away_percentage": str(
                        round((data[sets[1].format(i)] * 100) / set_total_points)
                    )
                    + "%",
                }
            except:
                continue

    def update(self, home: int, away: int, current_set: int):
        """Updates the stats with the current data of the match"""
        try:
            set_total_points = home + away
            self.sets["Set_" + str(current_set)] = {
                "Total_points": set_total_points,
                "Home_points": home,
                "Away_points": away,
                "Home_percentage": str(round((home * 100) / set_total_points)) + "%",
                "Away_percentage": str(round((away * 100) / set_total_points)) + "%",
            }
            self._total()
        except:
            pass

    def _total(self):
        try:
            self.total = {
                "Total_points": 0,
                "Home_points": 0,
                "Away_points": 0,
                "Home_percentage": "0",
                "Away_percentage": "0",
            }
            for x in self.sets.keys():
                data = self.sets[x]
                self.total["Total_points"] += data["Total_points"]
                self.total["Home_points"] += data["Home_points"]
                self.total["Away_points"] += data["Away_points"]
            self.total["Home_percentage"] = (
                str(
                    round(
                        (self.total["Home_points"] * 100) / self.total["Total_points"]
                    )
                )
                + "%"
            )
            self.total["Away_percentage"] = (
                str(
                    round(
                        (self.total["Away_points"] * 100) / self.total["Total_points"]
                    )
                )
                + "%"
            )
        except:
            pass

    def _match_history(self,m_id,h_id,a_id):
        URL = "{}/MatchStatistics.aspx?mID={}".format(self.league_url,m_id)
        r = requests.get(URL)
        self.comp_id= r.url.split('ID=')[-1]
        
        soup = BeautifulSoup(r.content, 'lxml')
        idin=soup.find_all('div', attrs = {'id':'RPL_HisotryMatches'})
        won=[]
        for x in idin:
            result = x.find('span', attrs = {'id':'LB_SetResult'}).text.replace(" ","").split('-')
            home = int((x.find('span', attrs = {'id':'LB_SetResult'}).parent.parent.parent.parent).find('input', attrs = {'id':'HF_HomeTeamID'})['value'])
            away = int((x.find('span', attrs = {'id':'LB_SetResult'}).parent.parent.parent.parent).find('input', attrs = {'id':'HF_GuestTeamID'})['value'])
            if result[0]>result[1]:
                if home == h_id:
                    won.append(home)
                elif home == a_id:
                    won.append(home)
            elif result[1]>result[0]:
                if away == h_id:
                    won.append(away)
                elif away == a_id:
                    won.append(away)
    
        won_home = str(won.count(h_id)) if len(won) > 0 else "No Encontrado"
        won_away = str(won.count(a_id)) if len(won) > 0 else "No Encontrado"
        self.match_history={
            'played': str(len(won)) if len(won) > 0 else "No Encontrado",
            'won_home': won_home,
            'won_away': won_away,
        }
        teams_stats=self._team_stats(h_id,a_id)
        self.home=teams_stats['home']
        self.away=teams_stats['away']
        
    def _team_stats(self,home,away):
        teams_stats = {
            'home':{
                'played': 0,
                'won': 0,
                'lost': 0,
                'set_total': 0,
                'set_won': 0,
                'set_lost': 0,
                'set_percent': 0,
                'points_total': 0,
                'points_won': 0,
                'points_lost': 0,
                'points_percent': 0,
                'result_30': 0,
                'result_31': 0,
                'result_32': 0,
                'result_23': 0,
                'result_13': 0,
                'result_03': 0,
                },
            'away':{
                'played': 0,
                'won': 0,
                'lost': 0,
                'set_total': 0,
                'set_won': 0,
                'set_lost': 0,
                'set_percent': 0,
                'points_total': 0,
                'points_won': 0,
                'points_lost': 0,
                'points_percent': 0,
                'result_30': 0,
                'result_31': 0,
                'result_32': 0,
                'result_23': 0,
                'result_13': 0,
                'result_03': 0,
                },
        }
        URL = "{}/CompetitionStandings.aspx?ID={}".format(self.league_url,self.comp_id)
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'lxml')
        for k,i in {'home':home,'away':away}.items():
            tables=soup.find_all('input', attrs = {'value':str(i)})
            for x in tables:
                teams_stats[k]['played'] += int(x.parent.parent.find('span', attrs = {'id':'MatchesPlayed'}).text) if x.parent.parent.find('span', attrs = {'id':'MatchesPlayed'}) != None else 0
                teams_stats[k]['won'] += int(x.parent.parent.find('span', attrs = {'id':'WonMatches'}).text) if x.parent.parent.find('span', attrs = {'id':'WonMatches'}) != None else 0
                teams_stats[k]['lost'] += int(x.parent.parent.find('span', attrs = {'id':'LostMatches'}).text) if x.parent.parent.find('span', attrs = {'id':'LostMatches'}) != None else 0
                teams_stats[k]['set_total'] += int(x.parent.parent.find('span', attrs = {'id':'SetsWon'}).text)+int(x.parent.parent.find('span', attrs = {'id':'SetsLost'}).text) if x.parent.parent.find('span', attrs = {'id':'SetsWon'}) != None else 0
                teams_stats[k]['set_won'] += int(x.parent.parent.find('span', attrs = {'id':'SetsWon'}).text) if x.parent.parent.find('span', attrs = {'id':'SetsWon'}) != None else 0
                teams_stats[k]['set_lost'] += int(x.parent.parent.find('span', attrs = {'id':'SetsLost'}).text) if x.parent.parent.find('span', attrs = {'id':'SetsLost'}) != None else 0
                teams_stats[k]['points_total'] += int(x.parent.parent.find('span', attrs = {'id':'PuntiFatti'}).text)+int(x.parent.parent.find('span', attrs = {'id':'PuntiSubiti'}).text) if x.parent.parent.find('span', attrs = {'id':'PuntiFatti'}) != None else 0
                teams_stats[k]['points_won'] += int(x.parent.parent.find('span', attrs = {'id':'PuntiFatti'}).text) if x.parent.parent.find('span', attrs = {'id':'PuntiFatti'}) != None else 0
                teams_stats[k]['points_lost'] += int(x.parent.parent.find('span', attrs = {'id':'PuntiSubiti'}).text) if x.parent.parent.find('span', attrs = {'id':'PuntiSubiti'}) != None else 0
                teams_stats[k]['result_30'] += int(x.parent.parent.find('span', attrs = {'id':'Final30'}).text) if x.parent.parent.find('span', attrs = {'id':'Final30'}) != None else 0
                teams_stats[k]['result_31'] += int(x.parent.parent.find('span', attrs = {'id':'Final31'}).text) if x.parent.parent.find('span', attrs = {'id':'Final31'}) != None else 0
                teams_stats[k]['result_32'] += int(x.parent.parent.find('span', attrs = {'id':'Final32'}).text) if x.parent.parent.find('span', attrs = {'id':'Final32'}) != None else 0
                teams_stats[k]['result_23'] += int(x.parent.parent.find('span', attrs = {'id':'Final23'}).text) if x.parent.parent.find('span', attrs = {'id':'Final23'}) != None else 0
                teams_stats[k]['result_13'] += int(x.parent.parent.find('span', attrs = {'id':'Final13'}).text) if x.parent.parent.find('span', attrs = {'id':'Final13'}) != None else 0
                teams_stats[k]['result_03'] += int(x.parent.parent.find('span', attrs = {'id':'Final03'}).text) if x.parent.parent.find('span', attrs = {'id':'Final03'}) != None else 0
            teams_stats[k]['set_percent'] = round((teams_stats[k]['set_won']*100)/teams_stats[k]['set_total'])
            teams_stats[k]['points_percent'] = round((teams_stats[k]['points_won']*100)/teams_stats[k]['points_total'])
        return teams_stats
    
class PlayerStats:
    def __init__(self,player_id:int,team_id:int) -> None:
        self.id=player_id
        self.team_id=team_id
        self.points=0
        self.serve={
            "Out": 0,
            "Win": 0,
            "Error": 0,
            "Total": 0,
        }
        self.reception={
            "Win": 0,
            "Error": 0,
            "Total": 0,
        }
        self.block={
            "Win": 0,
        }
        self.attack = {
            "Win": 0,
            "Error": 0,
            "Total": 0,
        }

    def _update(self,data):
        for player in data:
            if player['PID'] == self.id:
                self.points = player['PS']
                self.serve={
                    "Out": player['SOut'],
                    "Win": player['SWin'],
                    "Error": player['SErr'],
                    "Total": player['STot'],
                }
                self.reception={
                    "Win": player['RWin'],
                    "Error": player['RErr'],
                    "Total": player['RTot'],
                }
                self.block={
                    "Win": player['BWin'],
                }
                self.attack = {
                    "Win": player['SpWin'],
                    "Error": player['SpErr'],
                    "Total": player['SpTot'],
                }