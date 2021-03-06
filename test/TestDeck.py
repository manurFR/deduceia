import unittest
from Deck import prepare_deck, resolve_murder_card, deal_deck, calculate_rounds, format_card, format_hand, \
    draw_question_cards, Range, parse_card, discard_question_cards, next_card, determine_murderer
from GameState import GameState
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

    def test_resolve_murder_card_for_a_nine(self):
        self.assertEqual((9, '$'), resolve_murder_card((1, '$'), (8, '$')))
        self.assertEqual((9, 'H'), resolve_murder_card((8, 'L'), (1, '$')))

    def test_next_card_for_a_regular_card(self):
        self.assertEqual((3, 'H'), next_card((2, 'H')))

    def test_next_card_for_a_nine(self):
        self.assertEqual((1, '$'), next_card((9, '$')))

    def test_deal_deck(self):
        players = [HumanPlayer('test'), AIPlayer('joe')]
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

    def test_parse_card(self):
        self.assertEqual((5, 'L'), parse_card('5L'))

    def test_draw_question_cards(self):
        state = GameState()
        state.interrogation_deck = [(8, 'H'), (3, '$'), (1, '$'), (1, 'L')]

        draw_question_cards(state)
        self.assertItemsEqual([(1, 'L'), (1, '$'), (3, '$')], state.question_cards)
        self.assertEqual([(8, 'H')], state.interrogation_deck)

    def test_draw_question_cards_when_there_are_not_enough_cards_in_the_interrogation_deck(self):
        state = GameState()
        state.interrogation_deck = [(4, 'L')]
        state.discard_deck = [(3, '$'), (6, 'H'), (7, 'L')]

        draw_question_cards(state)
        self.assertEqual(3, len(state.question_cards))
        self.assertIn((4, 'L'), state.question_cards)
        self.assertEqual(0, len(state.discard_deck))
        self.assertEqual(1, len(state.interrogation_deck))

    def test_discard_question_cards(self):
        state = GameState()
        state.question_cards = [(2, 'H'), (7, 'H'), (5, '$')]
        state.discard_deck = []
        discard_question_cards(state.question_cards, state.discard_deck)
        self.assertEqual([(2, 'H'), (7, 'H'), (5, '$')], state.discard_deck)
        self.assertEqual([], state.question_cards)

    def test_determine_murderer_when_its_another_player(self):
        state = GameState()
        john = HumanPlayer('john')
        jim = AIPlayer('jim')
        jack = AIPlayer('jack')
        state.current_player = john
        state.players = [john, jim, jack]
        state.extra_card = (8, 'L')

        john._hand = [(5, 'L'), (9, 'H'), (6, '$')]
        jim._hand = [(4, 'L'), (7, 'L'), (3, '$')]
        jack._hand = [(1, 'L'), (3, 'H'), (5, '$')]

        accusation_cards = [(5, 'L'), (7, '$')]  # => murder card = 3H
        self.assertEqual(jack, determine_murderer(state, accusation_cards))

    def test_determine_murderer_when_its_the_extra_card_and_the_next_is_the_current_player(self):
        state = GameState()
        john = HumanPlayer('john')
        jim = AIPlayer('jim')
        jack = AIPlayer('jack')
        state.current_player = john
        state.players = [john, jim, jack]
        state.extra_card = (4, 'L')

        john._hand = [(5, 'L'), (9, 'H'), (6, '$')]
        jim._hand = [(4, 'L'), (6, 'L'), (3, '$')]
        jack._hand = [(1, 'L'), (3, 'H'), (5, '$')]

        accusation_cards = [(1, 'L'), (3, 'L')]  # => murder card = 4L
        self.assertEqual(jim, determine_murderer(state, accusation_cards))

    def test_determine_murderer_when_there_is_no_extra_card(self):
        state = GameState()
        john = HumanPlayer('john')
        jim = AIPlayer('jim')
        jack = AIPlayer('jack')
        state.current_player = john
        state.players = [john, jim, jack]
        state.extra_card = None

        john._hand = [(5, 'L'), (9, 'H'), (6, '$')]
        jim._hand = [(4, 'L'), (7, 'L'), (3, '$')]
        jack._hand = [(1, 'L'), (3, 'H'), (5, '$')]

        accusation_cards = [(5, 'L'), (7, '$')]  # => murder card = 3H
        self.assertEqual(jack, determine_murderer(state, accusation_cards))


class TestRange(unittest.TestCase):
    def test_suits_has_the_common_suit_when_both_cards_are_the_same_suit(self):
        self.assertEqual(['H'], (Range((1, 'H'), (7, 'H'))).suits)

    def test_suits_is_always_all_suits_when_cards_are_of_different_suits(self):
        self.assertEqual(['L', 'H', '$'], Range((3, 'L'), (3, 'H')).suits)

    def test_ranks_is_as_expected_when_the_low_card_is_lower_than_the_high_card(self):
        self.assertEqual([6, 7, 8, 9], Range((6, 'L'), (9, '$')).ranks)

    def test_ranks_extend_around_the_corner_when_the_low_card_is_higher_than_the_high_card(self):
        self.assertEqual([8, 9, 1, 2, 3], Range((8, '$'), (3, '$')).ranks)

    def test_range_is_all_three_numbers_when_the_low_card_is_the_same_as_the_high_card_with_different_suits(self):
        card_range = Range((5, '$'), (5, 'L'))
        self.assertEqual([5], card_range.ranks)
        self.assertEqual(['L', 'H', '$'], card_range.suits)

    def test_range_requires_choice_when_both_cards_are_the_same(self):
        with self.assertRaises(AssertionError):
            card_range = Range((4, 'H'), (4, 'H'))

    def test_range_requires_valid_choice_when_both_cards_are_the_same(self):
        with self.assertRaises(AssertionError):
            card_range = Range((4, 'H'), (4, 'H'), choice='RANKS')

    def test_range_is_all_suits_when_both_cards_are_the_same_and_choice_is_rank(self):
        card_range = Range((4, 'H'), (4, 'H'), choice='rank')
        self.assertEqual(['L', 'H', '$'], card_range.suits)
        self.assertEqual([4], card_range.ranks)

    def test_range_is_all_ranks_when_both_cards_are_the_same_and_choice_is_suit(self):
        card_range = Range((4, 'H'), (4, 'H'), choice='suit')
        self.assertEqual(['H'], card_range.suits)
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9], card_range.ranks)

    def test_range_provides_an_iterator(self):
        card_range = Range((3, 'L'), (4, 'H'))
        iterator = iter(card_range)

        self.assertEqual((3, 'L'), iterator.next())
        self.assertEqual((3, 'H'), iterator.next())
        self.assertEqual((3, '$'), iterator.next())
        self.assertEqual((4, 'L'), iterator.next())
        self.assertEqual((4, 'H'), iterator.next())
        self.assertEqual((4, '$'), iterator.next())
        with self.assertRaises(StopIteration):
            iterator.next()

    def test_range_provides_a_readable_str(self):
        self.assertEqual("3L->5$", str(Range((3, 'L'), (5, '$'))))
        self.assertEqual("3L->3L [rank]", str(Range((3, 'L'), (3, 'L'), choice='rank')))

    def test_range_provides_the_list_of_cards(self):
        self.assertEqual([(8, 'L'), (9, 'L'), (1, 'L')], Range((8, 'L'), (1, 'L')).cards())


if __name__ == '__main__':
    unittest.main()
