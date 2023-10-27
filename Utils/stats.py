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

    def _scrap_stats(self):
        URL = "https://livosur-web.dataproject.com/MatchStatistics.aspx?mID={}".format(6020)
        r = requests.get(URL) 
        
        soup = BeautifulSoup(r.content, 'lxml') 
        table = soup.find('tr', attrs = {'id':'__0'})
        idin=soup.find_all('div', attrs = {'id':'RPL_HisotryMatches'})
        for x in idin:
            print(x.find('span', attrs = {'id':'LB_SetResult'}))

Stats()._scrap_stats()