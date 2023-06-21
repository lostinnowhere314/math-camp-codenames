import time

import numpy as np
from bidict import bidict


embeddings = np.load('embeddings.npz')
embeddings = {word[1:]: tuple(embeddings[word]) for word in embeddings.files} # Hack to remove underscore from beginning of words
embeddings = bidict(embeddings)

SPREAD = 10
MAX_DISTANCE = 5.0

def get_embedding(word):
    word = word.lower().strip().replace(" ", "_")
    try:
        return np.array(embeddings[word])
    except KeyError:
        print(f"I don't know the word: {word}")
        raise

def get_board_matrix(board):
    remaining_words = board.get_unrevealed_words()
    return np.array([get_embedding(word) for word in remaining_words])

# def get_closest_words(board, clue, num_guesses):
#     board_matrix = get_board_matrix(board)
#     clue_embedding = get_embedding(clue)
    
#     # Cosine similarity
#     similarity = (board_matrix @ clue_embedding) / (np.linalg.norm(board_matrix, axis=1) * np.linalg.norm(clue_embedding))
#     similarity = np.nan_to_num(similarity)

#     # Sort by similarity
#     sorted_indices = np.argsort(similarity)[::-1]
#     sorted_words = [get_word(board_matrix[i]) for i in sorted_indices]

#     # print([f"{word}: {similarity[sorted_indices[i]]}" for i, word in enumerate(sorted_words)][:10])

#     return sorted_words[:num_guesses]

def get_closest_words(board, clue, num_guesses):
    board_matrix = get_board_matrix(board)
    clue_embedding = get_embedding(clue)

    # Euclidean distance
    distance = np.linalg.norm(board_matrix - clue_embedding, axis=1)

    # Sort by distance
    sorted_indices = np.argsort(distance)
    sorted_words = [get_word(board_matrix[i]) for i in sorted_indices]

    print([f"{word}: {distance[sorted_indices[i]]}" for i, word in enumerate(sorted_words)][:10])

    return sorted_words[:num_guesses]

def give_clue(player):
    team_name = player.get_team().get_name()
    board = player.game.board
    
    board.print_spymaster_view()

    poss_clues = list(set(embeddings.keys()) - set(board.get_unrevealed_words()))
    poss_clues_matrix = np.array([get_embedding(clue) for clue in poss_clues]) # Shape is (poss_clues, embedding_dim)

    board_words = board.get_unrevealed_words()
    board_teams = [board.get_card(word).get_owner() for word in board_words]
    board_reward = np.array([1 if team == team_name else 0 for team in board_teams]) # Shape is (board_words,)
    board_matrix = np.array([get_embedding(word) for word in board_words]) # Shape is (board_words, embedding_dim)

    # Find euclidean distance between clues and board words
    distances = np.linalg.norm(board_matrix[:, None, :] - poss_clues_matrix[None, :, :], axis=2) # Shape is (board_words, poss_clues)

    # Remove clues that are too far away
    good_clues = np.min(distances, axis=0) < MAX_DISTANCE
    poss_clues = np.array(poss_clues)[good_clues]
    distances = distances[:, good_clues]

    # Calculate score
    score = np.exp(-distances**2/SPREAD**2) * board_reward[:, None] # Shape is (board_words, poss_clues)
    score = np.sum(score, axis=0) # Shape is (poss_clues,)

    # Sort by score
    best_clue = poss_clues[np.argmax(score)]

    print(f"Clue: {best_clue}")
    print(f"Score: {score[np.argmax(score)]}")
    print(f"Distances: {distances[:, np.argmax(score)]}")
    return best_clue, 1

def get_word(embedding):
    return embeddings.inv[tuple(embedding)]

def guess_words(player, clue, num_guesses):
    best_words = get_closest_words(player.game.board, clue, num_guesses)
    best_words.reverse()

    for reamining_guesses in range(num_guesses + 1, 0, -1):
        print(f"{reamining_guesses} guesses remaining")
        best_word = best_words.pop()
        time.sleep(1)
        print(f"Guessing word: {best_word}")
        card = player.game.board.get_card(best_word)
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
        
        if len(best_words) == 0:
            print("Stopping guessing")
            return

# def guess_words(player, clue, num_guesses):
#     player.game.board.print_operative_view()
#     print(f"Clue: {clue} - {num_guesses}")
#     if num_guesses == 0:
#         num_guesses = len(player.game.board.get_unrevealed_words()) - 1
#     else:
#         num_guesses = min(num_guesses, len(player.game.board.get_unrevealed_words()) - 1)
#     for reamining_guesses in range(num_guesses + 1, 0, -1):
#         print(f"{reamining_guesses} guesses remaining")
#         card = choose_card(player)
#         card.reveal()
#         player.game.board.print_operative_view()
#         if card.get_owner() == player.get_team().get_name():
#             print("Correct!")
#             if player.game.board.get_num_cards_remaining_by_owner(player.get_team().get_name()) == 0:
#                 player.team.win()
#                 return
#         elif card.get_owner() == "ASSASSIN":
#             print("You guessed the assassin! Your team loses!")
#             player.team.lose()
#             return
#         elif card.get_owner() == "CIVILIAN":
#             print("You guessed a civilian! Your turn is over.")
#             return
#         else:
#             print("Incorrect!")
#             if player.game.board.get_num_cards_remaining_by_owner(card.get_owner()) == 0:
#                 player.game.get_team_by_name(card.get_owner()).win()
#                 return
        
#         if reamining_guesses > 1:
#             keep_guessing = yn_input("Keep guessing? (y/n) ")
#             if not keep_guessing:
#                 return