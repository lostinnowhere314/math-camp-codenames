class Team:
    def __init__(self, name, spymaster, operative):
        self.name = name
        self.spymaster = spymaster
        self.operative = operative
        self.spymaster.set_team(self)
        self.operative.set_team(self)
        self.status = "PLAYING"
        self.game = None
    
    def set_game(self, game):
        self.game = game
        self.spymaster.set_game(game)
        self.operative.set_game(game)
    
    def get_game(self):
        return self.game
    
    def get_name(self):
        return self.name
    
    def get_spymaster(self):
        return self.spymaster
    
    def get_operative(self):
        return self.operative
    
    def set_status(self, status):
        self.status = status
    
    def get_status(self):
        return self.status
    
    def lose(self):
        self.status = "LOST"
    
    def win(self):
        self.status = "WON"
