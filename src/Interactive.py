from collections import OrderedDict
import sys

from Deck import format_hand, format_card, Range, parse_card, determine_murderer


CANCEL = "**CANCEL**"
HIDDEN = "**HIDDEN**"


def ask_for(prompt, wanted_type=unicode, allowed=[]):
    while True:
        response = raw_input(prompt)
        if len(allowed) > 0 and response not in allowed:
            print '> Invalid answer (allowed : {0})'.format('/'.join(allowed))
        else:
            return wanted_type(response)


def ask_for_a_card_or_cancel(label, allowed_cards=[]):
    while True:
        card = ask_for('Select {0} card (or \'cancel\'): '.format(label), unicode, allowed_cards)
        if card == 'cancel':
            return CANCEL
        try:
            return parse_card(card)
        except AssertionError:  # string not parsable as a card
            pass  # try again


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
    low_card = ask_for_a_card_or_cancel('low', allowed_cards)
    if low_card == CANCEL:
        return False  # turn not ended
    allowed_cards.remove(format_card(low_card))
    high_card = ask_for_a_card_or_cancel('high', allowed_cards)
    if high_card == CANCEL:
        return False  # turn not ended
    choice = None
    if low_card == high_card:
        choice = ask_for('Identical cards. Choose rank or suit: ', str, ['rank', 'suit', 'cancel'])
        if choice == 'cancel':
            return False  # turn not ended
    card_range = Range(low_card, high_card, choice=choice)
    result = opponent.cards_in_range(card_range)
    print "Cards in this range: {0}".format(result)
    state.history.append({'turn':      state.turn,
                          'player':    state.current_player,
                          'action':    'interrogate',
                          'opponent':  opponent,
                          'range':     card_range,
                          'result':    result})
    return True  # turn ended


def secret_command(state):
    print
    print "Secret"
    opponent = choose_an_opponent(state)
    low_card = ask_for_a_card_or_cancel('low')
    if low_card == CANCEL:
        return False  # turn not ended
    high_card = ask_for_a_card_or_cancel('high')
    if high_card == CANCEL:
        return False  # turn not ended
    choice = None
    if low_card == high_card:
        choice = ask_for('Identical cards. Choose rank or suit: ', unicode, ['rank', 'suit', 'cancel'])
        if choice == 'cancel':
            return False  # turn not ended
    card_range = Range(low_card, high_card, choice=choice)
    result = opponent.cards_in_range(card_range)
    print "Cards in this range: {0}".format(result)
    state.history.append({'turn':      state.turn,
                          'player':    state.current_player,
                          'action':    'secret',
                          'opponent':  opponent,
                          'range':     card_range,
                          'result':    result})
    return True  # turn ended


def maxlength_by_column(data, columns, headers=True):
    if headers:
        # the default minimum length is the length of the key since it will be displayed as the header
        maxlength = OrderedDict((column, len(column)) for column in columns)
    else:
        maxlength = OrderedDict.fromkeys(columns, 0)

    for row in data:
        for key, value in row.iteritems():
            if key in maxlength and value != HIDDEN:
                maxlength[key] = max(maxlength[key], len(str(value)))

    # returns [length1, length2] in the same order ['key1', 'key2', ...] as input argument 'columns'
    return maxlength.values()


def print_tabular_data(data, columns, maxlength, headers=True):
    assert len(columns) == len(maxlength)
    fmt_string = '  '.join('{' + column + ':<' + str(length) + '}' for column, length in zip(columns, maxlength))
    if headers:
        print fmt_string.format(**dict((header, header.capitalize()) for header in columns))  # header line
    for row in data:
        for key, value in row.iteritems():
            if value == HIDDEN:
                row[key] = '*' * maxlength[columns.index(key)]
        print fmt_string.format(**row)


def print_history(state):
    print
    if len(state.history) == 0:
        print "No turns to display"
        return
    # preprocess
    data = []
    for row in state.history:
        if row['action'] == 'interrogate':
            data.append({'turn':     row['turn'],
                         'player':   row['player'].name,
                         'opponent': row['opponent'].name,
                         'range':    row['range'],
                         'result':   row['result'],
                         'note':     ''})
        elif row['action'] == 'secret':
            if state.current_player in [row['player'], row['opponent']]:
                # Secrets can be seen only by prosecutor and witness
                data.append({'turn':     row['turn'],
                             'player':   row['player'].name,
                             'opponent': row['opponent'].name,
                             'range':    row['range'],
                             'result':   row['result'],
                             'note':     '(Secret)'})
            else:
                data.append({'turn':     row['turn'],
                             'player':   row['player'].name,
                             'opponent': row['opponent'].name,
                             'range':    HIDDEN,
                             'result':   HIDDEN,
                             'note':     '(Secret)'})

    accusations = []
    for row in state.accusations:
        accusations.append({'fill':    '    ',
                            'player':  row['player'].name,
                            'accused': row['accused'].name,
                            'cards':   ' '.join(format_card(card) for card in row['cards']),
                            'result':  row['outcome']})

    columns = ['turn', 'player', 'opponent', 'range', 'result', 'note']

    print "History"
    maxlength = maxlength_by_column(data, columns)
    print_tabular_data(data, columns, maxlength)
    print
    print "Accusations"
    maxlength.pop()  # remove the last length (for 'note') that we don't use
    print_tabular_data(accusations, ['fill', 'player', 'accused', 'cards', 'result'], maxlength, headers=False)

    return False  # turn not ended


def accuse_command(state):
    print
    print "Accuse"
    opponent = choose_an_opponent(state)
    first_card = ask_for_a_card_or_cancel('the first')
    if first_card == CANCEL:
        return False  # turn not ended
    second_card = ask_for_a_card_or_cancel('the second')
    if second_card == CANCEL:
        return False  # turn not ended
    print
    accusation_cards = [first_card, second_card]
    player_to_accuse = determine_murderer(state, accusation_cards)
    if opponent == player_to_accuse and sorted(accusation_cards) == sorted(state.evidence_cards):
        outcome = 'correct'
    else:
        outcome = 'incorrect'
    print 'Your guess is: {0}'.format(outcome.capitalize())
    state.accusations.append({'player':   state.current_player,
                              'accused':  opponent,
                              'cards':    accusation_cards,
                              'outcome':  outcome})


    return True  # turn ended