from .stats import PlayerStats
class Player:
    def __init__(self, league:str, team_id:int, player_id:int, ply_name:str, ply_num:int) -> None:
        self.team_id= team_id
        self.id = player_id
        self.name= ply_name
        self.number= ply_num
        self.stats = PlayerStats(player_id,team_id)
        self.photo = "https://images.dataproject.com/{}/TeamPlayer/1080/1080/TeamPlayer_{}_{}.jpg".format(league,self.team_id,self.id)