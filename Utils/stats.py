import requests 
from bs4 import BeautifulSoup

class Stats:
    def __init__(self) -> None:
        self.total = {
            "Total_points": 0,
            "Home_points": 0,
            "Away_points": 0,
            "Home_percentage": "0",
            "Away_percentage": "0",
        }
        self.sets = {}
        pass

    def initiate(self, data, current_set):
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

    def _match_history(self,h_id,a_id):
        URL = "https://livosur-web.dataproject.com/MatchStatistics.aspx?mID={}".format(6088)
        r = requests.get(URL) 
        
        soup = BeautifulSoup(r.content, 'lxml') 
        idin=soup.find_all('div', attrs = {'id':'RPL_HisotryMatches'})
        won=[]
        for x in idin:
            result = x.find('span', attrs = {'id':'LB_SetResult'}).text.replace(" ","").split('-')
            home = (x.find('span', attrs = {'id':'LB_SetResult'}).parent.parent.parent.parent).find('input', attrs = {'id':'HF_HomeTeamID'})['value']
            away = (x.find('span', attrs = {'id':'LB_SetResult'}).parent.parent.parent.parent).find('input', attrs = {'id':'HF_GuestTeamID'})['value']
            if result[0]>result[1] and home == h_id:
                won.append(home)
            elif away == a_id:
                won.append(away)
        print(won)

Stats()._scrap_stats()