import codenames
import codenames.human_player

import ai_player

def main():
    spymaster = codenames.player.Player("Human", codenames.human_player.give_clue, codenames.human_player.guess_words)
    ## Uncomment to play with your AI version
    spymaster = codenames.player.Player("AI", ai_player.give_clue, None)
    
    operative = codenames.player.Player("Human", codenames.human_player.give_clue, codenames.human_player.guess_words)

    # Set up and start the game with one player
    team = codenames.Team("Red", spymaster, operative)
    game = codenames.Game([team], num_words=9)
    game.play()

if __name__ == "__main__":
    main()
