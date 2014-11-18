from random import choice
from Deck import hand_sorter, SUITS, Range, format_card
from Interactive import ask_for, help_command, quit_command, print_summary, interrogate_command, print_history, \
    secret_command, accuse_command
from Sheet import EVIDENCE_CARDS, Sheet

COMMANDS = {'h': help_command,
            'r': print_summary,
            't': print_history,
            'i': interrogate_command,
            's': secret_command,
            'a': accuse_command,
            'q': quit_command}


class Player(object):

    def __init__(self, name):
        self._name = name
        self._hand = []
        self._low_suit = None
        self._secret = 1

    def deal_card(self, card):
        self._hand.append(card)
        self._hand.sort(key=hand_sorter)

    def lowest_suits(self):
        # first count how many cards for each suit
        suits = dict((s, 0) for s in SUITS)
        for card in self.hand:
            suits[card[1]] += 1

        # next determine which suits have the smallest number of cards
        lowest_suits = []
        smallest_number = len(self.hand)
        for suit, number in suits.iteritems():
            if number <= smallest_number:
                if number < smallest_number:
                    lowest_suits = []
                    smallest_number = number
                lowest_suits.append(suit)
        return lowest_suits

    def set_low_suit(self, suit):
        self._low_suit = suit

    def cards_in_range(self, card_range):
        return len([card for card in iter(card_range) if card in self.hand])

    def use_secret(self):
        self._secret -= 1

    @property
    def name(self):
        return self._name

    @property
    def hand(self):
        return self._hand

    @property
    def low_suit(self):
        return self._low_suit

    @property
    def secret(self):
        return self._secret


class HumanPlayer(Player):

    def play_turn(self, state):
        # here self == human_player
        turn_ended = False
        while not turn_ended:
            command = ask_for('Your choice (h for help): ', str, COMMANDS.keys())
            if COMMANDS[command] is not None:
                turn_ended = COMMANDS[command](state)
                print

    # noinspection PyMethodMayBeStatic
    def is_human(self):
        return True


class AIPlayer(Player):
    NAMES = ['Amy', 'Ben', 'Clara', 'Don', 'Emma', 'Fred', 'Gina', 'Harry', 'Isa', 'Jim', 'Kat', 'Leo', 'Mia', 'Ned',
             'Otis', 'Peggy', 'Rita', 'Sam', 'Tara', 'Vic', 'Walt', 'Yun', 'Zoe']

    def choose_low_suit(self, lowest_suits):
        # choose the low suit to reveal between two or three possible choices
        self.set_low_suit(choice(lowest_suits))

    def play_turn(self, state):
        other_players = list(state.players)
        other_players.remove(self)

        action = 'interrogate'
        opponent, cards = self.choose_option(state, other_players)

        card_range = Range(*cards)
        result = opponent.cards_in_range(card_range)

        print "Interrogate player: {0}".format(opponent.name)
        if len(cards) == 3:
            print "Low card: {0} High card: {1} [{2}]".format(format_card(cards[0]), format_card(cards[1]), cards[2])
        else:
            print "Low card: {0} High card: {1}".format(format_card(cards[0]), format_card(cards[1]))
        print "Cards in this range: {0}".format(result)
        state.history.append({'turn':      state.turn,
                              'player':    state.current_player,
                              'action':    'interrogate',
                              'opponent':  opponent,
                              'range':     card_range,
                              'result':    result})

    def choose_option(self, state, other_players):
        card_pairs = self.prepare_card_pairs(state.question_cards)
        return choice(other_players), choice(card_pairs)

    def prepare_card_pairs(self, question_cards):
        card_pairs = set()
        for index_low, low_card in enumerate(question_cards):
            for index_high, high_card in enumerate(question_cards):
                if index_low != index_high:
                    if low_card == high_card:  # identical cards
                        card_pairs.add((low_card, high_card, 'rank'))
                        card_pairs.add((low_card, high_card, 'suit'))
                    else:
                        card_pairs.add((low_card, high_card))
        return list(card_pairs)

    # noinspection PyMethodMayBeStatic
    def is_human(self):
        return False

    # noinspection PyAttributeOutsideInit
    def setup_ai(self, other_players):
        self.sheets = {EVIDENCE_CARDS: Sheet(EVIDENCE_CARDS)}
        for player in other_players:
            self.sheets[player] = Sheet(player.name)
