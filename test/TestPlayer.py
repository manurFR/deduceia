import unittest

from Deck import Range
from GameState import GameState
from Player import HumanPlayer, Player, AIPlayer
from Sheet import EVIDENCE_CARDS
from TestUtils import sheet_table


class TestPlayer(unittest.TestCase):
    def test_hand_is_sorted(self):
        player = HumanPlayer('test')
        for card in [(2, '$'), (9, 'L'), (8, 'H'), (2, 'H'), (4, 'L')]:
            player.deal_card(card)

        self.assertEqual([(4, 'L'), (9, 'L'), (2, 'H'), (8, 'H'), (2, '$')], player.hand)

    def test_hand_with_one_lowest_suit(self):
        player = HumanPlayer('test')
        for card in [(2, '$'), (9, 'L'), (8, 'H'), (2, 'H'), (4, 'L')]:
            player.deal_card(card)

        self.assertEqual(['$'], player.lowest_suits())

    def test_hand_with_two_lowest_suit(self):
        player = HumanPlayer('test')
        for card in [(2, '$'), (9, 'H'), (8, 'H'), (2, 'H'), (4, 'L')]:
            player.deal_card(card)

        self.assertItemsEqual(['$', 'L'], player.lowest_suits())

    def test_hand_with_three_lowest_suit(self):
        player = HumanPlayer('test')
        for card in [(2, '$'), (9, 'H'), (8, '$'), (2, 'H'), (4, 'L'), (5, 'L')]:
            player.deal_card(card)

        self.assertItemsEqual(['L', '$', 'H'], player.lowest_suits())

    def test_lowest_suits_when_a_suit_has_no_cards(self):
        player = HumanPlayer('test')
        for card in [(2, '$'), (8, '$'), (2, 'H')]:
            player.deal_card(card)

        self.assertItemsEqual(['L'], player.lowest_suits())

    def test_no_cards_in_range(self):
        player = Player('jim')
        for card in [(2, '$'), (8, '$'), (4, 'L'), (5, 'L')]:
            player.deal_card(card)

        card_range = Range((6, 'L'), (7, 'H'))  # 6 & 7 for all suits

        self.assertEqual(0, player.cards_in_range(card_range))

    def test_cards_in_range_more_than_zero(self):
        player = Player('john')
        for card in [(4, 'L'), (5, 'L'), (2, 'H'), (5, 'H'), (9, 'H'), (2, '$'), (8, '$'), ]:
            player.deal_card(card)

        card_range = Range((1, 'H'), (7, 'H'))  # 1 to 7 of hate

        self.assertEqual(2, player.cards_in_range(card_range))

    def test_prepare_card_pairs(self):
        player = AIPlayer('Ella')
        self.assertItemsEqual([((1, 'L'), (2, 'H')), ((1, 'L'), (3, '$')), ((2, 'H'), (3, '$')),
                               ((2, 'H'), (1, 'L')), ((3, '$'), (1, 'L')), ((3, '$'), (2, 'H'))],
                              player.prepare_card_pairs([(1, 'L'), (2, 'H'), (3, '$')]))

    def test_prepare_card_pairs_should_include_rank_and_suit_for_identical_cards(self):
        player = AIPlayer('Ella')
        pairs = player.prepare_card_pairs([(1, 'L'), (1, 'L'), (3, '$')])
        self.assertItemsEqual([((1, 'L'), (1, 'L'), 'rank'), ((1, 'L'), (1, 'L'), 'suit'),
                               ((1, 'L'), (3, '$')), ((3, '$'), (1, 'L'))], pairs)


class TestAI(unittest.TestCase):
    def setUp(self):
        self.thor = AIPlayer('thor')
        self.sigrid = AIPlayer('sigrid')
        self.erlend = HumanPlayer('erlend')

        self.state = GameState()
        self.state.players = [self.thor, self.sigrid, self.erlend]

    def test_ai_player_setup_ai(self):
        self.thor._hand = [(1, 'L'), (8, '$')]
        self.sigrid._hand = [(7, 'L'), (4, 'H')]
        self.erlend._hand = [(9, 'H'), (9, '$')]

        self.state.extra_card = (5, 'L')
        self.thor.setup_ai(self.state)

        expected_sheet = sheet_table(excluded=[(1, 'L'), (8, '$'), (5, 'L')])

        self.assertEqual(expected_sheet, self.thor.sheets['evidence'].table)
        self.assertEqual(expected_sheet, self.thor.sheets[self.sigrid].table)
        self.assertEqual(expected_sheet, self.thor.sheets[self.erlend].table)

    def test_ai_player_setup_ai_when_there_is_no_extra_card(self):
        self.state.extra_card = None

        try:
            self.thor.setup_ai(self.state)
        except TypeError:
            self.fail("When there is no extra card, setup_ai() should not raise an exception")

    def test_review_last_turn_marks_cards_as_excluded_when_result_is_zero(self):
        self.state.history.append({'turn': 1,
                                   'player': self.thor,
                                   'action': 'interrogate',
                                   'opponent': self.sigrid,
                                   'range': Range((2, 'H'), (6, 'H')),
                                   'result': 0})

        self.thor.setup_ai(self.state)
        self.thor.review_turn(self.state, -1)

        self.assertEqual(sheet_table(excluded=[(2, 'H'), (3, 'H'), (4, 'H'), (5, 'H'), (6, 'H')]),
                         self.thor.sheets[self.sigrid].table)

    def test_review_last_turn_does_nothing_if_opponent_is_self(self):
        self.state.history.append({'turn': 1,
                                   'player': self.sigrid,
                                   'action': 'interrogate',
                                   'opponent': self.thor,
                                   'range': Range((2, 'H'), (6, 'H')),
                                   'result': 0})

        self.thor.setup_ai(self.state)
        try:
            self.thor.review_turn(self.state, -1)
        except KeyError:
            self.fail("review_last_interrogate() has tried to modify the player's own sheet")

    def test_review_last_turn_marks_cards_as_owned_when_results_equals_all_unknown_slots(self):
        self.thor._hand = [(5, 'H')]

        self.state.history.append({'turn': 1,
                                   'player': self.thor,
                                   'action': 'interrogate',
                                   'opponent': self.sigrid,
                                   'range': Range((2, 'H'), (6, 'H')),
                                   'result': 4})

        self.thor.setup_ai(self.state)
        self.thor.review_turn(self.state, -1)

        self.assertEqual(sheet_table(excluded=[(5, 'H')], owned=[(2, 'H'), (3, 'H'), (4, 'H'), (6, 'H')]),
                         self.thor.sheets[self.sigrid].table)
        self.assertEqual(sheet_table(excluded=[(5, 'H'), (2, 'H'), (3, 'H'), (4, 'H'), (6, 'H')]),
                         self.thor.sheets[self.erlend].table)
        self.assertEqual(sheet_table(excluded=[(5, 'H'), (2, 'H'), (3, 'H'), (4, 'H'), (6, 'H')]),
                         self.thor.sheets[EVIDENCE_CARDS].table)

    def test_review_last_turn_takes_secret_into_account_if_current_player_was_the_asker(self):
        self.state.history.append({'turn': 1,
                                   'player': self.thor,
                                   'action': 'secret',
                                   'opponent': self.sigrid,
                                   'range': Range((9, '$'), (2, '$')),
                                   'result': 0})

        self.thor.setup_ai(self.state)
        self.thor.review_turn(self.state, -1)

        self.assertEqual(sheet_table(excluded=[(9, '$'), (1, '$'), (2, '$')]),
                         self.thor.sheets[self.sigrid].table)

        self.state.history.append({'turn': 2,
                                   'player': self.erlend,
                                   'action': 'secret',
                                   'opponent': self.sigrid,
                                   'range': Range((3, 'L'), (3, '$')),
                                   'result': 0})

        self.thor.review_turn(self.state, -1)

        self.assertEqual(sheet_table(excluded=[(9, '$'), (1, '$'), (2, '$')]),
                         self.thor.sheets[self.sigrid].table)

    def test_review_turn_gives_suit_total(self):
        self.state.history.append({'turn': 1,
                                   'player': self.thor,
                                   'action': 'interrogate',
                                   'opponent': self.sigrid,
                                   'range': Range((2, '$'), (8, '$')),
                                   'result': 2})

        self.thor.setup_ai(self.state)
        self.thor.sheets[self.sigrid].exclude_cards([(1, '$'), (4, '$')])
        self.thor.sheets[self.sigrid].own_cards([(9, '$')])

        self.thor.review_turn(self.state, -1)

        self.assertEqual(sheet_table(excluded=[(1, '$'), (4, '$')], owned=[(9, '$')], totals={'$': 3}),
                         self.thor.sheets[self.sigrid].table)

    def test_review_turn_gives_rank_total(self):
        self.state.history.append({'turn': 1,
                                   'player': self.thor,
                                   'action': 'interrogate',
                                   'opponent': self.sigrid,
                                   'range': Range((3, 'L'), (3, 'H')),
                                   'result': 2})

        self.thor.setup_ai(self.state)
        self.thor.review_turn(self.state, -1)

        self.assertEqual(sheet_table(totals={3: 2}), self.thor.sheets[self.sigrid].table)


    def test_review_history_full(self):
        self.state.history.append({'turn': 1, 'player': self.thor, 'action': 'interrogate', 'opponent': self.sigrid,
                                   'range': Range((9, '$'), (2, '$')), 'result': 0})
        self.state.history.append({'turn': 2, 'player': self.sigrid, 'action': 'interrogate', 'opponent': self.erlend,
                                   'range': Range((2, '$'), (2, 'L')), 'result': 0})
        self.state.history.append({'turn': 3, 'player': self.erlend, 'action': 'interrogate', 'opponent': self.sigrid,
                                   'range': Range((3, 'L'), (4, 'H')), 'result': 4})

        self.thor._hand = [(3, '$'), (4, 'L')]

        self.thor.setup_ai(self.state)
        self.thor.review_history(self.state)

        self.assertEqual(sheet_table(excluded=[(9, '$'), (1, '$'), (2, '$'), (3, '$'), (4, 'L')],
                                     owned=[(3, 'L'), (3, 'H'), (4, '$'), (4, 'H')]),
                         self.thor.sheets[self.sigrid].table)
        self.assertEqual(sheet_table(excluded=Range((2, 'L'), (4, '$')).cards(), totals={2: 0}),
                         self.thor.sheets[self.erlend].table)

    def test_review_totals_suit_total_equals_owned_slots(self):
        self.thor.setup_ai(self.state)

        self.thor.sheets[self.sigrid].own_cards([(3, '$'), (8, '$')])
        self.thor.sheets[self.sigrid].set_suit_total('$', 2)

        self.thor.review_totals()

        self.assertEqual(sheet_table(excluded=[(1, '$'), (2, '$'), (4, '$'), (5, '$'), (6, '$'), (7, '$'), (9, '$')],
                                     owned=[(3, '$'), (8, '$')], totals={'$': 2}),
                         self.thor.sheets[self.sigrid].table)

    def test_review_totals_suit_total_equals_zero(self):
        self.thor.setup_ai(self.state)

        self.thor.sheets[self.sigrid].set_suit_total('L', 0)

        self.thor.review_totals()

        self.assertEqual(sheet_table(excluded=Range((1, 'L'), (9, 'L')).cards(), totals={'L': 0}),
                         self.thor.sheets[self.sigrid].table)

    def test_review_totals_suit_total_equals_number_of_owned_plus_unknown_slots(self):
        self.thor.setup_ai(self.state)

        self.thor.sheets[self.sigrid].own_cards([(3, 'L')])
        self.thor.sheets[self.sigrid].exclude_cards([(1, 'L'), (2, 'L'), (5, 'L'), (6, 'L'), (8, 'L'), (9, 'L')])
        self.thor.sheets[self.sigrid].set_suit_total('L', 3)

        self.thor.review_totals()

        self.assertEqual(sheet_table(excluded=[(1, 'L'), (2, 'L'), (5, 'L'), (6, 'L'), (8, 'L'), (9, 'L')],
                                     owned=[(3, 'L'), (4, 'L'), (7, 'L')], totals={'L': 3}),
                         self.thor.sheets[self.sigrid].table)

    def test_review_totals_does_nothing_with_suit_total_when_its_larger_than_owned_slots(self):
        self.thor.setup_ai(self.state)

        self.thor.sheets[self.sigrid].own_cards([(3, 'L')])
        self.thor.sheets[self.sigrid].exclude_cards([(1, 'L'), (2, 'L')])
        self.thor.sheets[self.sigrid].set_suit_total('L', 5)

        self.thor.review_totals()

        self.assertEqual(sheet_table(excluded=[(1, 'L'), (2, 'L')], owned=[(3, 'L')], totals={'L': 5}),
                         self.thor.sheets[self.sigrid].table)

    def test_review_totals_rank_total_equals_owned_slots(self):
        self.thor.setup_ai(self.state)

        self.thor.sheets[self.sigrid].own_cards([(3, 'H'), (3, '$')])
        self.thor.sheets[self.sigrid].set_rank_total(3, 2)

        self.thor.review_totals()

        self.assertEqual(sheet_table(excluded=[(3, 'L')], owned=[(3, 'H'), (3, '$')], totals={3: 2}),
                         self.thor.sheets[self.sigrid].table)

    def test_review_totals_rank_total_equals_zero(self):
        self.thor.setup_ai(self.state)

        self.thor.sheets[self.sigrid].set_rank_total(5, 0)

        self.thor.review_totals()

        self.assertEqual(sheet_table(excluded=[(5, 'L'), (5, 'H'), (5, '$')], totals={5: 0}),
                         self.thor.sheets[self.sigrid].table)

    def test_review_totals_rank_total_equals_number_of_owned_plus_unknown_slots(self):
        self.thor.setup_ai(self.state)

        self.thor.sheets[self.sigrid].own_cards([(5, 'L')])
        self.thor.sheets[self.sigrid].exclude_cards([(5, '$')])
        self.thor.sheets[self.sigrid].set_rank_total(5, 2)

        self.thor.review_totals()

        self.assertEqual(sheet_table(excluded=[(5, '$')], owned=[(5, 'L'), (5, 'H')], totals={5: 2}),
                         self.thor.sheets[self.sigrid].table)

    def test_review_totals_does_nothing_with_rank_total_when_its_larger_than_owned_slots(self):
        self.thor.setup_ai(self.state)

        self.thor.sheets[self.sigrid].own_cards([(3, 'L')])
        self.thor.sheets[self.sigrid].exclude_cards([(3, 'H')])
        self.thor.sheets[self.sigrid].set_rank_total(3, 3)

        self.thor.review_totals()

        self.assertEqual(sheet_table(excluded=[(3, 'H')], owned=[(3, 'L')], totals={3: 3}),
                         self.thor.sheets[self.sigrid].table)


if __name__ == '__main__':
    unittest.main()
