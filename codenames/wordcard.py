class WordCard:
    def __init__(self, word, owner):
        self.word = word
        self.owner = owner
        self.revealed = False

    def __str__(self):
        return f"{self.word} ({self.owner})" if self.revealed else f"{self.word} (?)"

    def __repr__(self):
        return f"WordCard({self.word}, {self.owner})"

    def reveal(self):
        self.revealed = True

    def is_revealed(self):
        return self.revealed

    def get_word(self):
        return self.word

    def get_owner(self):
        return self.owner
    
    def print_spymaster_view(self):
        print(f"{self.word} ({self.owner})")
    
    def print_operative_view(self):
        if self.revealed:
            print(f"{self.word} ({self.owner})")
        else:
            print(f"{self.word} (?)")
