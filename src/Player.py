from random import choice
from Deck import hand_sorter, SUITS


class Player(object):

    def __init__(self):
        self._hand = []
        self._low_suit = None

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

    @property
    def name(self):
        return self._name

    @property
    def hand(self):
        return self._hand

    @property
    def low_suit(self):
        return self._low_suit


class HumanPlayer(Player):

    def __init__(self, name):
        super(HumanPlayer, self).__init__()
        self._name = name

    def is_human(self):
        return True


class AIPlayer(Player):

    def __init__(self, id):
        super(AIPlayer, self).__init__()
        self._name = 'AI#{0}'.format(id)

    def choose_low_suit(self, lowest_suits):
        # choose the low suit to reveal between two or three possible choices
        self.set_low_suit(choice(lowest_suits))

    def is_human(self):
        return False
