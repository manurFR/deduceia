import unittest
from Deck import Range
from GameState import GameState
from Player import HumanPlayer, Player, AIPlayer


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
        print pairs
        self.assertItemsEqual([((1, 'L'), (1, 'L'), 'rank'), ((1, 'L'), (1, 'L'), 'suit'),
                               ((1, 'L'), (3, '$')), ((3, '$'), (1, 'L'))], pairs)

    def test_ai_player_setup_ai(self):
        thor = AIPlayer('Thor')
        sigrid = AIPlayer('Sigrid')
        erlend = HumanPlayer('Erlend')

        state = GameState()
        state.players = [thor, sigrid, erlend]
        thor._hand = [(1, 'L'), (8, '$')]
        sigrid._hand = [(7, 'L'), (4, 'H')]
        erlend._hand = [(9, 'H'), (9, '$')]

        state.extra_card = (5, 'H')

        thor.setup_ai(state)

        expected_sheet = {'L': {1:  0, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1, 'total': -1},
                          'H': {1: -1, 2: -1, 3: -1, 4: -1, 5:  0, 6: -1, 7: -1, 8: -1, 9: -1, 'total': -1},
                          '$': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8:  0, 9: -1, 'total': -1},
                          'total': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1}}
        self.assertEqual(expected_sheet, thor.sheets['evidence'].table)
        self.assertEqual(expected_sheet, thor.sheets[sigrid].table)
        self.assertEqual(expected_sheet, thor.sheets[erlend].table)

    def test_review_last_interrogate_marks_cards_as_excluded_when_result_is_zero(self):
        thor = AIPlayer('Thor')
        sigrid = AIPlayer('Sigrid')

        state = GameState()
        state.players = [thor, sigrid]
        state.extra_card = (1, 'L')
        state.history.append({'turn':      1,
                              'player':    thor,
                              'action':    'interrogate',
                              'opponent':  sigrid,
                              'range':     Range((2, 'H'), (6, 'H')),
                              'result':    0})

        thor.setup_ai(state)
        thor.review_last_interrogate(state)

        expected_sheet_for_sigrid = {'L': {1:  0, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1, 'total': -1},
                                     'H': {1: -1, 2:  0, 3:  0, 4:  0, 5:  0, 6:  0, 7: -1, 8: -1, 9: -1, 'total': -1},
                                     '$': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1, 'total': -1},
                                     'total': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1}}
        self.assertEqual(expected_sheet_for_sigrid, thor.sheets[sigrid].table)

    def test_review_last_interrogate_does_nothing_if_opponent_is_self(self):
        thor = AIPlayer('Thor')
        sigrid = AIPlayer('Sigrid')

        state = GameState()
        state.players = [thor, sigrid]
        state.extra_card = (1, 'L')
        state.history.append({'turn':      1,
                              'player':    sigrid,
                              'action':    'interrogate',
                              'opponent':  thor,
                              'range':     Range((2, 'H'), (6, 'H')),
                              'result':    0})

        thor.setup_ai(state)
        try:
            thor.review_last_interrogate(state)
        except KeyError:
            self.fail("review_last_interrogate() has tried to modify the player's own sheet")


if __name__ == '__main__':
    unittest.main()
