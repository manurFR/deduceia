import Deck

MISS = 0   # we know the subject doesn't own this card
VOID = -1  # we don't know whether the subject owns this card or not
OWND = 1   # we know the subject DOES own that card

TOTAL = "total"
UNKNOWN = VOID

EVIDENCE_CARDS = "evidence"


class Sheet(object):
    def __init__(self, subject):
        self.subject = subject

        self.table = {}
        for suit in Deck.SUITS:
            self.table[suit] = {TOTAL: UNKNOWN}
            for rank in Deck.RANKS:
                self.table[suit][rank] = VOID
        self.table[TOTAL] = dict((rank, UNKNOWN) for rank in Deck.RANKS)  # initialize totals for ranks

        self.grand_total = UNKNOWN

    def exclude_cards(self, cards):
        if not isinstance(cards, list):
            cards = [cards]
        for card in cards:
            self.table[card[1]][card[0]] = MISS

    def own_cards(self, cards):
        if not isinstance(cards, list):
            cards = [cards]
        for card in cards:
            self.table[card[1]][card[0]] = OWND