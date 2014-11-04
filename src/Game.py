from random import shuffle

from Deck import prepare_deck, deal_deck, draw_question_cards, discard_question_cards, resolve_murder_card, \
    next_card
from GameState import GameState
from Player import HumanPlayer, AIPlayer
from Interactive import ask_for, print_summary, print_low_suit, print_question_cards


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


def determine_low_suit(state):
    for player in state.players:
        lowest_suits = player.lowest_suits()
        if len(lowest_suits) == 1:
            player.set_low_suit(lowest_suits[0])
        elif player.is_human():
            str_choices = ' or '.join(lowest_suits)
            low_suit = ask_for('Which low suit do you want to reveal ({0}) ? '.format(str_choices), str, lowest_suits)
            player.set_low_suit(low_suit)
        else:
            player.choose_low_suit(lowest_suits)


def determine_murderer(state, accusation_cards):
    possible_murder_card = resolve_murder_card(*accusation_cards)
    while possible_murder_card in state.current_player.hand or possible_murder_card == state.extra_card:
        possible_murder_card = next_card(possible_murder_card)
    for player in state.players:
        if possible_murder_card in player.hand:
            return player
    raise ValueError  # one should not arrive here


def play_turn(state):
    id_current_player = state.turn % len(state.players)
    state.current_player = state.players[id_current_player]
    other_players = []
    for i in range(1, len(state.players)):
        other_players.append(state.players[(id_current_player + i) % len(state.players)])

    state.question_cards = draw_question_cards(state.interrogation_deck, state.discard_deck)
    print
    print 'Turn {0} - {1}'.format(state.turn, state.current_player.name)
    print_question_cards(state)
    state.current_player.play_turn(state)
    discard_question_cards(state.question_cards, state.discard_deck)
    state.turn += 1


def main():
    print 'Welcome to Deduce or Die! IA'
    print
    nb_players = ask_for('Number of players : ', int, ['3', '4', '5', '6'])
    human_player_name = ask_for('Type your name : ')

    state = GameState()

    players, state.human_player = prepare_players(nb_players, human_player_name)
    state.players = players

    motive_deck = prepare_game_deck(nb_decks=1)

    state.interrogation_deck = prepare_game_deck(nb_decks=2)
    state.discard_deck = []

    state.evidence_cards = [motive_deck.pop(), motive_deck.pop()]

    deal_deck(motive_deck, players)

    assert len(motive_deck) <= 1

    if len(motive_deck) == 1:
        state.extra_card = motive_deck[0]
    else:
        state.extra_card = None

    print_summary(state)

    determine_low_suit(state)
    print
    print_low_suit(players)

    state.turn = 1
    while True:
        play_turn(state)


if __name__ == '__main__':
    main()