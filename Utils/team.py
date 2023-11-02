class Team:
    def __init__(self, name: str, id: int, points: int, sets: int, players:dict, coach:str, logo:str) -> None:
        self.name = name
        self.id = id
        self.points = points
        self.sets = sets
        self.players = players
        self.coach = coach
        self.logo = logo
        pass
