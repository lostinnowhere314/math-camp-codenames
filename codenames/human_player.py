from . import board

def int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter an integer.")

def yn_input(prompt):
    while True:
        response = input(prompt).lower()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        else:
            print("Please enter 'y' or 'n'.")

def give_clue(player):
    player.game.board.print_spymaster_view()
    clue = input("Enter a clue: ")
    num_guesses = int_input("Enter the number of guesses: ")

    return clue, num_guesses

def choose_card(player):
    while True:
        try:
            word = input("Enter a word to guess: ")
            card = player.game.board.get_card(word)
            return card
        except board.CardNotOnBoardError:
            print("That word is not on the board.")
    

def guess_words(player, clue, num_guesses):
    player.game.board.print_operative_view()
    print(f"Clue: {clue} - {num_guesses}")
    if num_guesses == 0:
        num_guesses = len(player.game.board.get_unrevealed_words()) - 1
    else:
        num_guesses = min(num_guesses, len(player.game.board.get_unrevealed_words()) - 1)
    for reamining_guesses in range(num_guesses + 1, 0, -1):
        print(f"{reamining_guesses} guesses remaining")
        card = choose_card(player)
        card.reveal()
        player.game.board.print_operative_view()
        if card.get_owner() == player.get_team().get_name():
            print("Correct!")
            if player.game.board.get_num_cards_remaining_by_owner(player.get_team().get_name()) == 0:
                player.team.win()
                return
        elif card.get_owner() == "ASSASSIN":
            print("You guessed the assassin! Your team loses!")
            player.team.lose()
            return
        elif card.get_owner() == "CIVILIAN":
            print("You guessed a civilian! Your turn is over.")
            return
        else:
            print("Incorrect!")
            if player.game.board.get_num_cards_remaining_by_owner(card.get_owner()) == 0:
                player.game.get_team_by_name(card.get_owner()).win()
                return
        
        if reamining_guesses > 1:
            keep_guessing = yn_input("Keep guessing? (y/n) ")
            if not keep_guessing:
                return