import numpy as np

# Load the word embeddings
embeddings = np.load('embeddings.npz')
embeddings = {word: embeddings[word] for word in embeddings.files}

def get_embedding(word):
    """
    Take in the word and get the embedding out of the embeddings dictionary.
    Note that in this dictionary, each word has an underscore ("_") before it and
    all spaces are replaced by an underscore as well.
    """
    return None
    
def distance(vector1, vector2):
    """
    Return the distance between the two vectors
    (we'll talk about this on Thursday)
    """
    return None

def give_clue(player):
    """
    This is the function you will be writing.
    You will use the word embeddings to find words that
    are close to the words for your team on the board.
    """
    # Some examples of things you can do with the game
    team_name = player.get_team().get_name()
    unrevealed_cards = player.game.board.get_unrevealed_cards()
    possible_clues = embeddings.keys()
    
    # Card objects
    card = unrevealed_cards[0]
    card_word = card.word
    card_team = card.owner
    
    return None, 1
    
