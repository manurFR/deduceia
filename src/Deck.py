from random import shuffle

RANKS = range(1, 10)
SUITS = ['L', 'H', '$']
NB_QUESTION_CARDS = 3


def prepare_deck():
    return [(rank, suit) for rank in RANKS for suit in SUITS]


def resolve_murder_card(evidence1, evidence2):
    rank = (evidence1[0] + evidence2[0]) % len(RANKS)
    if rank == 0:
        rank = len(RANKS)
    if evidence1[1] == evidence2[1]:
        suit = evidence1[1]
    else:
        remaining_suit = list(SUITS)  # clone
        remaining_suit.remove(evidence1[1])
        remaining_suit.remove(evidence2[1])
        suit = remaining_suit[0]
    return rank, suit


def next_card(card):
    if card[0] == RANKS[-1]:
        return RANKS[0], card[1]
    else:
        return card[0]+1, card[1]


def calculate_rounds(deck, players):
    return len(deck) / len(players)


def deal_deck(deck, players):
    nb_rounds = calculate_rounds(deck, players)
    for _ in range(nb_rounds):
        for player in players:
            player.deal_card(deck.pop(0))


def format_card(card):
    return str(card[0]) + card[1]


def format_hand(cards):
    return ' '.join(format_card(card) for card in cards)


def parse_card(card):
    assert isinstance(card, basestring)
    assert len(card) == 2
    assert card[0].isdigit()
    assert int(card[0]) in RANKS
    assert card[1] in SUITS
    return int(card[0]), card[1]


def hand_sorter(card):
    return 10 * SUITS.index(card[1]) + card[0]


def draw_question_cards(state):
    state.question_cards = []

    if len(state.interrogation_deck) < NB_QUESTION_CARDS:
        state.question_cards.extend(state.interrogation_deck)
        state.interrogation_deck = list(state.discard_deck)  # clone !
        state.discard_deck = []
        shuffle(state.interrogation_deck)

    for _ in range(len(state.question_cards), NB_QUESTION_CARDS):
        state.question_cards.append(state.interrogation_deck.pop())
    state.question_cards.sort(key=hand_sorter)


def discard_question_cards(question_cards, discard_deck):
    discard_deck.extend(question_cards)
    del question_cards[:]


def determine_murderer(state, accusation_cards):
    possible_murder_card = resolve_murder_card(*accusation_cards)
    while possible_murder_card in state.current_player.hand or possible_murder_card == state.extra_card:
        possible_murder_card = next_card(possible_murder_card)
    for player in state.players:
        if possible_murder_card in player.hand:
            return player
    raise ValueError  # one should not arrive here


class Range(object):

    def __init__(self, low_card, high_card, choice=None):
        self.low_card = low_card
        self.high_card = high_card
        if low_card == high_card:
            assert choice in ['rank', 'suit']
            self.identical_cards = True
            self.choice = choice
        else:
            self.identical_cards = False

    @property
    def suits(self):
        if self.low_card[1] == self.high_card[1]:
            if self.identical_cards and self.choice == 'rank':
                return SUITS
            else:
                return [self.low_card[1]]
        else:
            return SUITS

    @property
    def ranks(self):
        if self.low_card[0] <= self.high_card[0]:
            if self.identical_cards and self.choice == 'suit':
                return RANKS
            else:
                return range(self.low_card[0], self.high_card[0] + 1)  # upper limit of range() is excluded
        elif self.low_card[0] > self.high_card[0]:  # wrap around the corner
            return range(self.low_card[0], len(RANKS) + 1) + range(1, self.high_card[0] + 1)

    def cards(self):
        return list(self)

    def __iter__(self):
        return iter((rank, suit) for rank in self.ranks for suit in self.suits)

    def __str__(self):
        return_str = '{0}->{1}'.format(format_card(self.low_card), format_card(self.high_card))
        if self.identical_cards:
            return_str += ' [{0}]'.format(self.choice)
        return return_str



