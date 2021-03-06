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

    def set_suit_total(self, suit, total):
        assert suit in Deck.SUITS
        self.table[suit][TOTAL] = total

    def set_rank_total(self, rank, total):
        assert rank in Deck.RANKS
        self.table[TOTAL][rank] = total

    def _filter(self, filter_status, filter_suit=None, filter_rank=None):
        cards = []
        for suit in self.table.keys():
            if (filter_suit is None and suit != TOTAL) or (suit == filter_suit):
                for rank, status in self.table[suit].iteritems():
                    if rank != TOTAL and status == filter_status and (filter_rank is None or rank == filter_rank):
                        cards.append((rank, suit))
        return cards

    def voids(self, suit=None, rank=None):
        return self._filter(filter_status=VOID, filter_suit=suit, filter_rank=rank)

    def owned(self, suit=None, rank=None):
        return self._filter(filter_status=OWND, filter_suit=suit, filter_rank=rank)

    def exclude_when_unknown_for_suit(self, suit):
        assert suit in Deck.SUITS

        for rank, status in self.table[suit].iteritems():
            if rank != TOTAL and status == VOID:
                self.table[suit][rank] = MISS

    def exclude_when_unknown_for_rank(self, rank):
        assert rank in Deck.RANKS

        for suit in Deck.SUITS:
            status = self.table[suit][rank]
            if status == VOID:
                self.table[suit][rank] = MISS

    def own_when_unknown_for_suit(self, suit):
        assert suit in Deck.SUITS

        for rank, status in self.table[suit].iteritems():
            if rank != TOTAL and status == VOID:
                self.table[suit][rank] = OWND

    def own_when_unknown_for_rank(self, rank):
        assert rank in Deck.RANKS

        for suit in Deck.SUITS:
            status = self.table[suit][rank]
            if status == VOID:
                self.table[suit][rank] = OWND