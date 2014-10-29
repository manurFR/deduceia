from random import shuffle
from Deck import prepare_deck
from Interactive import ask_for


def prepare_game_deck(nb_decks):
    deck = []
    for _ in range(nb_decks):
        deck.extend(prepare_deck())
    shuffle(deck)
    return deck


if __name__ == '__main__':
    print 'Welcome to Deduce or Die! IA'
    print
    nb_players = ask_for('Number of players : ', ['3', '4', '5', '6'])

    motive_deck = prepare_game_deck(nb_decks=1)
    interrogation_deck = prepare_game_deck(nb_decks=2)

    evidence1 = motive_deck.pop()
    evidence2 = motive_deck.pop()

