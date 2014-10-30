from random import shuffle

from Deck import prepare_deck, deal_deck, format_hand, format_card, draw_question_cards
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
    if human_player.low_suit:
        print_low_suit()
    print_secret()


def determine_low_suit():
    for player in players:
        lowest_suits = player.lowest_suits()
        if len(lowest_suits) == 1:
            player.set_low_suit(lowest_suits[0])
        elif player.is_human():
            str_choices = ' or '.join(lowest_suits)
            low_suit = ask_for('Which low suit do you want to reveal ({0}) ? '.format(str_choices), str, lowest_suits)
            player.set_low_suit(low_suit)
        else:
            player.choose_low_suit(lowest_suits)


def print_low_suit():
    str_low_suit = ''
    for player in players:
        str_low_suit += '[{0}: {1}] '.format(player.name, player.low_suit)
    print 'Low Suits: ' + str_low_suit


def print_secret():
    str_secret = ''
    for player in players:
        str_secret += '[{0}: {1}] '.format(player.name, player.secret)
    print 'Secret to play: ' + str_secret


def play_turn(turn_number):
    id_current_player = turn_number % len(players)
    current_player = players[id_current_player]
    other_players = []
    for i in range(1, len(players)):
        other_players.append(players[(id_current_player + i) % len(players)])

    question_cards = draw_question_cards(interrogation_deck, discard_deck)
    print
    print 'Turn {0}'.format(turn_number)
    print 'Question cards: {0}'.format(format_hand(question_cards))
    current_player.play_turn(question_cards, other_players)



if __name__ == '__main__':
    print 'Welcome to Deduce or Die! IA'
    print
    nb_players = ask_for('Number of players : ', int, ['3', '4', '5', '6'])
    human_player_name = ask_for('Type your name : ')

    players, human_player = prepare_players(nb_players, human_player_name)

    motive_deck = prepare_game_deck(nb_decks=1)
    interrogation_deck = prepare_game_deck(nb_decks=2)
    discard_deck = []

    evidence1 = motive_deck.pop()
    evidence2 = motive_deck.pop()

    deal_deck(motive_deck, players)

    assert len(motive_deck) <= 1

    if len(motive_deck) == 1:
        extra_card = motive_deck[0]
    else:
        extra_card = None

    print_summary()

    determine_low_suit()
    print
    print_low_suit()

    turn = 1
    while True:
        play_turn(turn)
        turn += 1
        if turn == 5:
            break
