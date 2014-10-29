from random import shuffle

from Deck import prepare_deck, deal_deck, format_hand, format_card
from Player import HumanPlayer, AIPlayer
from Interactive import ask_for


def prepare_game_deck(nb_decks):
    deck = []
    for _ in range(nb_decks):
        deck.extend(prepare_deck())
    shuffle(deck)
    return deck


def prepare_players(nb, player_name):
    human = HumanPlayer(player_name)
    list_players = [human]
    for i in range(1, nb):
        list_players.append(AIPlayer(i))
    shuffle(list_players)
    return list_players, human


def print_summary():
    print
    print "Game Summary"
    print "Your hand: {0}".format(format_hand(human_player.hand))
    if extra_card:
        print "Extra card: {0}".format(format_card(extra_card))


if __name__ == '__main__':
    print 'Welcome to Deduce or Die! IA'
    print
    nb_players = ask_for('Number of players : ', int, ['3', '4', '5', '6'])
    human_player_name = ask_for('Type your name : ')

    players, human_player = prepare_players(nb_players, human_player_name)

    motive_deck = prepare_game_deck(nb_decks=1)
    interrogation_deck = prepare_game_deck(nb_decks=2)

    evidence1 = motive_deck.pop()
    evidence2 = motive_deck.pop()

    deal_deck(motive_deck, players)

    assert len(motive_deck) <= 1

    if len(motive_deck) == 1:
        extra_card = motive_deck[0]
    else:
        extra_card = None

    print_summary()
    # TODO sort hand

