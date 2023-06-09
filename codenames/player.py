class Player:
    def __init__(self, name, give_clue_func, guess_words_func, team=None):
        self.name = name
        self.give_clue_func = give_clue_func
        self.guess_words_func = guess_words_func
        self.team = team
        self.game = None
    
    def get_name(self):
        return self.name

    def set_game(self, game):
        self.game = game
    
    def set_team(self, team):
        self.team = team
    
    def get_team(self):
        return self.team
    
    def give_clue(self):
        return self.give_clue_func(self)
    
    def guess_words(self, clue, num_guesses):
        return self.guess_words_func(self, clue, num_guesses)
    