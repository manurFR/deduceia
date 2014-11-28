from random import choice
from Deck import hand_sorter, SUITS, Range, format_card, RANKS
from Interactive import ask_for, help_command, quit_command, print_summary, interrogate_command, print_history, \
    secret_command, accuse_command
from Sheet import EVIDENCE_CARDS, Sheet, VOID, TOTAL, UNKNOWN

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
        other_players = state.players_except(self)

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
    def setup_ai(self, state):
        self.sheets = {EVIDENCE_CARDS: Sheet(EVIDENCE_CARDS)}
        for player in state.players:
            if player != self:
                self.sheets[player] = Sheet(player.name)

        for sheet in self.sheets.itervalues():
            if state.extra_card is not None:
                sheet.exclude_cards(state.extra_card)
            sheet.exclude_cards(self.hand)

    def review_last_interrogate(self, state):
        fact = state.history[-1]
        if fact['opponent'] == self:
            return  # we don't need to keep a sheet about ourselves
        if fact['action'] == 'secret' and fact['player'] != self:
            return  # secrets that the current player did not asked are not knwnon by him(her)

        if fact['result'] == 0:  # we are certain the opponent has no cards from the range
            self.sheets[fact['opponent']].exclude_cards(fact['range'].cards())

        unknown_slots = [card for card in fact['range'].cards() if card in self.sheets[fact['opponent']].voids()]
        if fact['result'] == len(unknown_slots):  # we are certain the opponent has all the unknown cards form the range
            self.sheets[fact['opponent']].own_cards(unknown_slots)
            for player in state.players_except(fact['opponent'], self):
                self.sheets[player].exclude_cards(unknown_slots)
            self.sheets[EVIDENCE_CARDS].exclude_cards(unknown_slots)

    def review_totals(self):
        for player in self.sheets.keys():
            table = self.sheets[player].table
            for suit in SUITS:
                if table[suit][TOTAL] != UNKNOWN:
                    if table[suit][TOTAL] == len(self.sheets[player].owned(suit=suit)):
                        self.sheets[player].exclude_when_void_for_suit(suit)
                    elif table[suit][TOTAL] == (len(self.sheets[player].owned(suit=suit)) +
                                                len(self.sheets[player].voids(suit=suit))):
                        self.sheets[player].own_when_void(suit)

            for rank in RANKS:
                if table[TOTAL][rank] != UNKNOWN:
                    if table[TOTAL][rank] == len(self.sheets[player].owned(rank=rank)):
                        self.sheets[player].exclude_when_void_for_rank(rank)
                    # elif table[suit][TOTAL] == len(self.sheets[player].owned(suit)) + len(self.sheets[player].voids(suit)):
                    #     self.sheets[player].own_when_void(suit)


