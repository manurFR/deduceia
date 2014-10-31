import sys
from Deck import format_hand, format_card


def ask_for(prompt, wanted_type=unicode, allowed=[]):
    while True:
        response = raw_input(prompt)
        if len(allowed) > 0 and response not in allowed:
            print '> Invalid answer (allowed : {0})'.format('/'.join(allowed))
        else:
            return wanted_type(response)


def help_command(*_):
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


def quit_command(*_):
    sure = ask_for('Are you sure [y/n] ? ')
    if sure.strip() == 'y':
        print "Bye."
        sys.exit(0)
    return False  # turn not ended


def print_summary(human_player, players, extra_card, *_):
    print
    print "Game Summary"
    print "Your hand: {0}".format(format_hand(human_player.hand))
    if extra_card:
        print "Extra card: {0}".format(format_card(extra_card))
    if human_player.low_suit:
        print_low_suit(players)
    print_secret(players)
    return False  # turn not ended


def print_low_suit(players):
    str_low_suit = ''
    for player in players:
        str_low_suit += '[{0}: {1}] '.format(player.name, player.low_suit)
    print 'Low Suits: ' + str_low_suit


def print_secret(players):
    str_secret = ''
    for player in players:
        str_secret += '[{0}: {1}] '.format(player.name, player.secret)
    print 'Secret to play: ' + str_secret