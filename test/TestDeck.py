import unittest
from Deck import prepare_deck, resolve_murder_card, deal_deck, calculate_rounds, format_card, format_hand, \
    draw_question_cards
from Player import HumanPlayer, AIPlayer


class TestDeck(unittest.TestCase):
    def test_prepare_deck(self):
        deck = prepare_deck()
        self.assertEqual(3*9, len(deck))
        self.assertEqual(9, len([card for card in deck if card[1] == 'L']))
        self.assertEqual(9, len([card for card in deck if card[1] == 'H']))
        self.assertEqual(9, len([card for card in deck if card[1] == '$']))

    def test_resolve_murder_card_determine_rank(self):
        self.assertEqual(3, resolve_murder_card((1, '$'), (2, 'L'))[0])
        self.assertEqual(6, resolve_murder_card((9, 'H'), (6, 'H'))[0])
        self.assertEqual(2, resolve_murder_card((7, '$'), (4, 'H'))[0])

    def test_resolve_murder_card_determine_suit(self):
        self.assertEqual('$', resolve_murder_card((1, '$'), (7, '$'))[1])
        self.assertEqual('$', resolve_murder_card((8, 'L'), (9, 'H'))[1])

    def test_deal_deck(self):
        players = [HumanPlayer('test'), AIPlayer(1)]
        deck = [(1, 'L'), (2, 'L'), (3, 'L'), (4, 'L'), (5, 'L')]

        deal_deck(deck, players)

        self.assertEqual([(1, 'L'), (3, 'L')], players[0].hand)
        self.assertEqual([(2, 'L'), (4, 'L')], players[1].hand)

        self.assertEqual([(5, 'L')], deck)

    def test_calculate_rounds_no_remaining_cards(self):
        players = ['p1', 'p2', 'p3']
        deck = ['card1', 'card2', 'card3'] * 2
        self.assertEqual(2, calculate_rounds(deck, players))

    def test_calculate_rounds_one_remaining_card(self):
        players = ['p1', 'p2', 'p3']
        deck = ['card1', 'card2', 'card3', 'card4']
        self.assertEqual(1, calculate_rounds(deck, players))

    def test_format_card(self):
        self.assertEqual('3H', format_card((3, 'H')))

    def test_format_hand(self):
        self.assertEqual('3H 8$ 4L', format_hand([(3, 'H'), (8, '$'), (4, 'L')]))

    def test_draw_question_cards(self):
        interrogation_deck = ['card1', 'card2', 'card3', 'card4']

        self.assertItemsEqual(['card2', 'card3', 'card4'], draw_question_cards(interrogation_deck, []))
        self.assertEqual(['card1'], interrogation_deck)

    def test_draw_question_cards_when_there_are_not_enough_cards_in_the_interrogation_deck(self):
        interrogation_deck = ['card1']
        discard_deck = ['card2', 'card3', 'card4']

        drawn_cards = draw_question_cards(interrogation_deck, discard_deck)
        self.assertEqual(3, len(drawn_cards))
        self.assertIn('card1', drawn_cards)
        self.assertEqual(0, len(discard_deck))
        self.assertEqual(1, len(interrogation_deck))


if __name__ == '__main__':
    unittest.main()
