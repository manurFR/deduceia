class AIPlayer(object):
    def __init__(self, id):
        self._name = 'AI #{0}'.format(id)
        self._hand = []

    def deal_card(self, card):
        self._hand.append(card)

    @property
    def name(self):
        return self._name

    @property
    def hand(self):
        return self._hand
