from random import shuffle

RANKS = range(1, 10)
SUITS = ['L', 'H', '$']
NB_QUESTION_CARDS = 3


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


def hand_sorter(card):
    return 10 * SUITS.index(card[1]) + card[0]


def draw_question_cards(interrogation_deck, discard_deck):
    question_cards = []

    if len(interrogation_deck) < NB_QUESTION_CARDS:
        question_cards.extend(interrogation_deck)
        interrogation_deck = list(discard_deck)  # clone !
        del discard_deck[:]                      # clear deck by reference !
        shuffle(interrogation_deck)

    for _ in range(len(question_cards), NB_QUESTION_CARDS):
        question_cards.append(interrogation_deck.pop())
    return question_cards
