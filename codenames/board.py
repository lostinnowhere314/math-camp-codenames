import random

from . import wordcard

class CardNotOnBoardError(Exception):
    pass

class Board:
    @staticmethod
    def random_board(num_words, teams, word_source="codenames.txt"):
        words = []
        with open(word_source) as f:
            while word := f.readline().strip().lower():
                if len(word) > 0:
                    words.append(word)
        words = random.sample(words, num_words)
        
        team_names = [team.get_name() for team in teams] + ["CIVILIAN"]
        card_owners = []
        for i in range(len(words) - 1):
            card_owners.append(team_names[i % len(team_names)])
        card_owners.append("ASSASSIN")
        random.shuffle(card_owners)

        cards = [wordcard.WordCard(word, owner) for word, owner in zip(words, card_owners)] # type: ignore

        return Board(cards)

    def __init__(self, cards):
        self.cards = cards
    
    def __str__(self):
        return "\n".join([str(card) for card in self.cards])
    
    def __repr__(self):
        return f"Board({self.cards})"
    
    def get_card(self, word):
        for card in self.cards:
            if card.get_word() == word:
                return card
        raise CardNotOnBoardError(f"Card with word '{word}' not on board")
    
    def get_unrevealed_cards(self):
        return [card for card in self.cards if not card.is_revealed()]
    
    def get_unrevealed_words(self):
        return [card.get_word() for card in self.get_unrevealed_cards()]
    
    def get_num_cards_remaining_by_owner(self, owner):
        count = 0
        for card in self.cards:
            if card.get_owner() == owner and not card.is_revealed():
                count += 1
        return count
    
    def print_spymaster_view(self):
        for card in self.cards:
            card.print_spymaster_view()

    def print_operative_view(self):
        for card in self.cards:
            card.print_operative_view()