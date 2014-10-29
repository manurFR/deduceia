from random import shuffle

from AIPlayer import AIPlayer
from Deck import prepare_deck, deal_deck
from HumanPlayer import HumanPlayer
from Interactive import ask_for


def prepare_game_deck(nb_decks):
    deck = []
    for _ in range(nb_decks):
        deck.extend(prepare_deck())
    shuffle(deck)
    return deck


def prepare_players(nb, player_name):
    list_players = [HumanPlayer(player_name)]
    for i in range(1, nb):
        list_players.append(AIPlayer(i))
    shuffle(list_players)
    return list_players


if __name__ == '__main__':
    print 'Welcome to Deduce or Die! IA'
    print
    nb_players = ask_for('Number of players : ', int, ['3', '4', '5', '6'])
    human_player_name = ask_for('Type your name : ')

    players = prepare_players(nb_players, human_player_name)

    motive_deck = prepare_game_deck(nb_decks=1)
    interrogation_deck = prepare_game_deck(nb_decks=2)

    evidence1 = motive_deck.pop()
    evidence2 = motive_deck.pop()

    deal_deck(motive_deck, players)

    if len(motive_deck) > 0:
        extra_card = motive_deck[0]
    else:
        extra_card = None

