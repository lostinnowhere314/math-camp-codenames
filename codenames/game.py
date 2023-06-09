import random

from . import board

class Game:
    def __init__(self, teams, num_words=25):
        self.teams = teams
        self.num_words = num_words
        self.board = board.Board.random_board(self.num_words, self.teams)
        self.winner = None

        for team in self.teams:
            team.set_game(self)
    
    def get_team_by_name(self, name):
        for team in self.teams:
            if team.get_name() == name:
                return team
        raise ValueError(f"Team with name '{name}' not found")
    
    def check_for_winner(self):
        if len(self.teams) > 1:
            num_lost = 0
            for team in self.teams:
                if team.get_status() == "LOST":
                    num_lost += 1
            if num_lost == len(self.teams) - 1:
                for team in self.teams:
                    if team.get_status() != "LOST":
                        self.winner = team
                        return True
        for team in self.teams:
            if team.get_status() == "WON":
                self.winner = team
                return True
        return False
    
    def play(self):
        game_in_progress = True
        while game_in_progress:
            game_in_progress = False
            for team in self.teams:
                if team.get_status() != "PLAYING":
                    continue
                game_in_progress = True

                print(f"{team.get_name()}'s turn")
                print(f"{team.get_spymaster().get_name()} is spymaster. Give a clue.")
                clue, num_guesses = team.get_spymaster().give_clue()

                print()
                print(f"{team.get_operative().get_name()} is operative. Guess words.")
                team.get_operative().guess_words(clue, num_guesses)

                if self.check_for_winner():
                    print(f"{self.winner.get_name()} wins!") # type: ignore
                
                print()
                print()
                print()
        print("Game over.")