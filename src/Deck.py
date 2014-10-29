RANKS = range(1, 10)
SUITS = ['L', 'H', '$']


def prepare_deck():
    return [(rank, suit) for rank in RANKS for suit in SUITS]


def resolve_murder_card(evidence1, evidence2):
    rank = (evidence1[0] + evidence2[0]) % len(RANKS)
    if evidence1[1] == evidence2[1]:
        suit = evidence1[1]
    else:
        remaining_suit = list(SUITS)  # clone
        remaining_suit.remove(evidence1[1])
        remaining_suit.remove(evidence2[1])
        suit = remaining_suit[0]
    return rank, suit


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