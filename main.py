import codenames.player
import codenames.human_player
import codenames.ai_player
import codenames.team
import codenames.game

def main():
    spymaster = codenames.player.Player("AI", codenames.ai_player.give_clue, codenames.ai_player.guess_words)
    operative = codenames.player.Player("Human", codenames.human_player.give_clue, codenames.human_player.guess_words)

    team = codenames.team.Team("Red", spymaster, operative)

    game = codenames.game.Game([team], num_words=9)
    game.play()

if __name__ == "__main__":
    main()
