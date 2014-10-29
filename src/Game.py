from random import shuffle
from AIPlayer import AIPlayer
from Deck import prepare_deck
from HumanPlayer import HumanPlayer
from Interactive import ask_for


def prepare_game_deck(nb_decks):
    deck = []
    for _ in range(nb_decks):
        deck.extend(prepare_deck())
    shuffle(deck)
    return deck


def prepare_players(nb, name_human):
    players = [HumanPlayer(name_human)]
    for i in range(1, nb):
        players.append(AIPlayer(i))
    return players


if __name__ == '__main__':
    print 'Welcome to Deduce or Die! IA'
    print
    nb_players = ask_for('Number of players : ', int, ['3', '4', '5', '6'])
    player_name = ask_for('Type your name : ')
    prepare_players(nb_players, player_name)

    motive_deck = prepare_game_deck(nb_decks=1)
    interrogation_deck = prepare_game_deck(nb_decks=2)

    evidence1 = motive_deck.pop()
    evidence2 = motive_deck.pop()

