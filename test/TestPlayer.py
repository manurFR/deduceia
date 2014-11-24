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
        self.state.extra_card = (5, 'L')
        self.state.players = [self.thor, self.sigrid, self.erlend]

    def test_ai_player_setup_ai(self):
        self.thor._hand = [(1, 'L'), (8, '$')]
        self.sigrid._hand = [(7, 'L'), (4, 'H')]
        self.erlend._hand = [(9, 'H'), (9, '$')]

        self.thor.setup_ai(self.state)

        expected_sheet = sheet_table(excluded=[(1, 'L'), (8, '$'), (5, 'L')])

        self.assertEqual(expected_sheet, self.thor.sheets['evidence'].table)
        self.assertEqual(expected_sheet, self.thor.sheets[self.sigrid].table)
        self.assertEqual(expected_sheet, self.thor.sheets[self.erlend].table)

    def test_review_last_interrogate_marks_cards_as_excluded_when_result_is_zero(self):
        self.state.history.append({'turn':      1,
                                   'player': self.thor,
                                   'action': 'interrogate',
                                   'opponent': self.sigrid,
                                   'range': Range((2, 'H'), (6, 'H')),
                                   'result': 0})

        self.thor.setup_ai(self.state)
        self.thor.review_last_interrogate(self.state)

        self.assertEqual(sheet_table(excluded=[(5, 'L'), (2, 'H'), (3, 'H'), (4, 'H'), (5, 'H'), (6, 'H')]),
                         self.thor.sheets[self.sigrid].table)

    def test_review_last_interrogate_does_nothing_if_opponent_is_self(self):
        self.state.history.append({'turn': 1,
                                   'player': self.sigrid,
                                   'action': 'interrogate',
                                   'opponent': self.thor,
                                   'range': Range((2, 'H'), (6, 'H')),
                                   'result': 0})

        self.thor.setup_ai(self.state)
        try:
            self.thor.review_last_interrogate(self.state)
        except KeyError:
            self.fail("review_last_interrogate() has tried to modify the player's own sheet")

    def test_review_last_interrogate_marks_cards_as_owned_when_results_equals_all_unknown_slots(self):
        self.thor._hand = [(5, 'H')]

        self.state.history.append({'turn': 1,
                                   'player': self.thor,
                                   'action': 'interrogate',
                                   'opponent': self.sigrid,
                                   'range': Range((2, 'H'), (6, 'H')),
                                   'result': 4})

        self.thor.setup_ai(self.state)
        self.thor.review_last_interrogate(self.state)

        self.assertEqual(sheet_table(excluded=[(5, 'L'), (5, 'H')], owned=[(2, 'H'), (3, 'H'), (4, 'H'), (6, 'H')]),
                         self.thor.sheets[self.sigrid].table)
        self.assertEqual(sheet_table(excluded=[(5, 'L'), (5, 'H'), (2, 'H'), (3, 'H'), (4, 'H'), (6, 'H')]),
                         self.thor.sheets[self.erlend].table)
        self.assertEqual(sheet_table(excluded=[(5, 'L'), (5, 'H'), (2, 'H'), (3, 'H'), (4, 'H'), (6, 'H')]),
                         self.thor.sheets[EVIDENCE_CARDS].table)

    def test_review_last_interrogate_takes_secret_into_account_if_current_player_was_the_asker(self):
        self.state.history.append({'turn': 1,
                                   'player': self.thor,
                                   'action': 'secret',
                                   'opponent': self.sigrid,
                                   'range': Range((9, '$'), (2, '$')),
                                   'result': 0})

        self.thor.setup_ai(self.state)
        self.thor.review_last_interrogate(self.state)

        self.assertEqual(sheet_table(excluded=[(5, 'L'), (9, '$'), (1, '$'), (2, '$')]),
                         self.thor.sheets[self.sigrid].table)

        self.state.history.append({'turn': 2,
                                   'player': self.erlend,
                                   'action': 'secret',
                                   'opponent': self.sigrid,
                                   'range': Range((3, 'L'), (3, '$')),
                                   'result': 0})

        self.thor.review_last_interrogate(self.state)

        self.assertEqual(sheet_table(excluded=[(5, 'L'), (9, '$'), (1, '$'), (2, '$')]),
                         self.thor.sheets[self.sigrid].table)

    def test_review_totals_suit_total_equal_owned_slots(self):
        self.thor.setup_ai(self.state)

        self.thor.sheets[self.sigrid].own_cards([(3, 'L'), (8, 'L')])
        self.thor.sheets[self.sigrid].set_suit_total('L', 2)

        self.thor.review_totals()

        self.assertEqual(sheet_table(excluded=[(1, 'L'), (2, 'L'), (4, 'L'), (5, 'L'), (6, 'L'), (7, 'L'), (9, 'L')],
                                     owned=[(3, 'L'), (8, 'L')], totals={'L': 2}),
                         self.thor.sheets[self.sigrid].table)






if __name__ == '__main__':
    unittest.main()
