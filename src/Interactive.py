from collections import OrderedDict
import sys

from Deck import format_hand, format_card, Range, parse_card


def ask_for(prompt, wanted_type=unicode, allowed=[]):
    while True:
        response = raw_input(prompt)
        if len(allowed) > 0 and response not in allowed:
            print '> Invalid answer (allowed : {0})'.format('/'.join(allowed))
        else:
            return wanted_type(response)


def help_command(_):
    print
    print "Commands:"
    print " [h] (help) this command"
    print " [r] (summary) print a summary of the current game state"
    print " [t] (history) print an history of player's interrogations since the game start"
    print " [i] (interrogate) use the question cards to interrogate another player"
    print " [s] (secret) play a secret interrogation of another player"
    print " [a] (accuse) accuse another player (only once per game !)"
    print " [q] (quit) quit game prematurely"
    return False  # turn not ended


def quit_command(_):
    sure = ask_for('Are you sure [y/n] ? ')
    if sure.strip() == 'y':
        print "Bye."
        sys.exit(0)
    return False  # turn not ended


def print_summary(state):
    print
    print "Game Summary"
    print "Your hand: {0}".format(format_hand(state.human_player.hand))
    if state.extra_card:
        print "Extra card: {0}".format(format_card(state.extra_card))
    if state.human_player.low_suit:
        print_low_suit(state.players)
    print_secret(state.players)
    # TODO add current turn & question cards
    return False  # turn not ended


def print_low_suit(players):
    str_low_suit = ''
    for player in players:
        str_low_suit += '[{0}: {1}] '.format(player.name, player.low_suit)
    print 'Low Suits: ' + str_low_suit.strip()


def print_secret(players):
    str_secret = ''
    for player in players:
        str_secret += '[{0}: {1}] '.format(player.name, player.secret)
    print 'Secret to play: ' + str_secret.strip()


def print_question_cards(state):
    print 'Question cards: {0}'.format(format_hand(state.question_cards))


def choose_an_opponent(state):
    opponents = OrderedDict()

    list_opponents = list(state.players)
    list_opponents.remove(state.current_player)
    list_opponents.sort(key=lambda o: o.id)

    for player in list_opponents:
        opponents[player.id] = player

    allowed = [str(_id) for _id in opponents.keys()]

    chosen_id = ask_for('Which opponent ? [{0}] '.format(' '.join(str(_id) + ':' + player.name
                                                                  for _id, player in opponents.iteritems())),
                        int, allowed)

    return opponents[chosen_id]

def interrogate_command(state):
    print
    print "Interrogate"
    print_question_cards(state)
    opponent = choose_an_opponent(state)
    allowed_cards = [format_card(card) for card in state.question_cards]
    allowed_cards.append('cancel')
    low_card = ask_for('Select low card (or \'cancel\'): ', str, allowed_cards)
    if low_card == 'cancel':
        return False  # turn not ended
    allowed_cards.remove(low_card)
    high_card = ask_for('Select high card (or \'cancel\'): ', str, allowed_cards)
    if high_card == 'cancel':
        return False  # turn not ended
    state.history.append({'turn': state.turn,
                          'player': state.current_player,
                          'action': 'interrogate',
                          'opponent': opponent,
                          'range': Range(parse_card(low_card), parse_card(high_card))})
    return True  # turn ended