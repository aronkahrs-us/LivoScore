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

    def _initiate(self,data,current_set):
        sets= ['Set{}Home','Set{}Guest']
        for i in range(1,current_set+1):
            try:
                set_total_points = data[sets[0].format(i)] + data[sets[1].format(i)]
                self.sets['Set_'+str(i)] = {
                    "Total_points": set_total_points,
                    "Home_points": data[sets[0].format(i)],
                    "Away_points": data[sets[1].format(i)],
                    "Home_percentage": str(round((data[sets[0].format(i)]*100)/set_total_points)) + "%",
                    "Away_percentage": str(round((data[sets[1].format(i)]*100)/set_total_points)) + "%",
                }
            except:
                continue

    def _update(self,home:int,away:int,current_set:int):
        """Updates the stats with the current data of the match"""
        try:
            set_total_points = home + away
            self.sets['Set_'+str(current_set)] = {
                "Total_points": set_total_points,
                "Home_points": home,
                "Away_points": away,
                "Home_percentage": str(round((home*100)/set_total_points)) + "%",
                "Away_percentage": str(round((away*100)/set_total_points)) + "%",
            }
            self._total()
        except:
            pass

    def _total(self):
        try:
            for x in self.sets.keys():
                data=self.sets[x]
                self.total['Total_points'] += data['Total_points']
                self.total['Total']['Home_points'] += data['Home_points']
                self.total['Total']['Away_points'] += data['Away_points']
            self.stats['Total']['Home_percentage'] = str(round((self.total['Home_points']*100)/self.total['Total_points'])) + "%"
            self.stats['Total']['Away_percentage'] = str(round((self.total['Away_points']*100)/self.total['Total_points'])) + "%"
        except:
            pass
