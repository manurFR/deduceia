class HumanPlayer(object):

    def __init__(self, name):
        self._name = name
        self._hand = []

    def deal_card(self, card):
        self._hand.append(card)

    @property
    def name(self):
        return self._name

    @property
    def hand(self):
        return self._hand
