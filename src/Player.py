class Player(object):

    def __init__(self):
        self._hand = []

    def deal_card(self, card):
        self._hand.append(card)

    @property
    def name(self):
        return self._name

    @property
    def hand(self):
        return self._hand


class HumanPlayer(Player):

    def __init__(self, name):
        super(HumanPlayer, self).__init__()
        self._name = name


class AIPlayer(Player):

    def __init__(self, id):
        super(AIPlayer, self).__init__()
        self._name = 'AI #{0}'.format(id)
