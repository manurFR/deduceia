import unittest

from Game import prepare_game_deck, prepare_players, determine_murderer
from GameState import GameState
from Player import HumanPlayer, AIPlayer


class TestGame(unittest.TestCase):
    def test_prepare_game_deck(self):
        self.assertEqual(3 * 9 * 3, len(prepare_game_deck(3)))

    def test_prepare_player_with_one_human_player(self):
        players, human_player = prepare_players(1, 'Test')
        self.assertIsInstance(players[0], HumanPlayer)
        self.assertEqual('Test', players[0].name)
        self.assertEqual(human_player, players[0])

    def test_prepare_player_with_three_players(self):
        players, _ = prepare_players(3, 'Test')
        self.assertEqual(3, len(players))
        self.assertEqual(['AIPlayer', 'AIPlayer', 'HumanPlayer'], sorted([type(player).__name__ for player in players]))
        self.assertEqual(['AI#1', 'AI#2', 'Test'], sorted([player.name for player in players]))

    def test_determine_murderer_when_its_another_player(self):
        state = GameState()
        john = HumanPlayer('john')
        ai1 = AIPlayer(1)
        ai2 = AIPlayer(2)
        state.current_player = john
        state.players = [john, ai1, ai2]
        state.extra_card = (8, 'L')

        john._hand = [(5, 'L'), (9, 'H'), (6, '$')]
        ai1._hand = [(4, 'L'), (7, 'L'), (3, '$')]
        ai2._hand = [(1, 'L'), (3, 'H'), (5, '$')]

        accusation_cards = [(5, 'L'), (7, '$')]  # => murder card = 3H
        self.assertEqual(ai2, determine_murderer(state, accusation_cards))

    def test_determine_murderer_when_its_the_extra_card_and_the_next_is_the_current_player(self):
        state = GameState()
        john = HumanPlayer('john')
        ai1 = AIPlayer(1)
        ai2 = AIPlayer(2)
        state.current_player = john
        state.players = [john, ai1, ai2]
        state.extra_card = (4, 'L')

        john._hand = [(5, 'L'), (9, 'H'), (6, '$')]
        ai1._hand = [(4, 'L'), (6, 'L'), (3, '$')]
        ai2._hand = [(1, 'L'), (3, 'H'), (5, '$')]

        accusation_cards = [(1, 'L'), (3, 'L')]  # => murder card = 4L
        self.assertEqual(ai1, determine_murderer(state, accusation_cards))

    def test_determine_murderer_when_there_is_no_extra_card(self):
        state = GameState()
        john = HumanPlayer('john')
        ai1 = AIPlayer(1)
        ai2 = AIPlayer(2)
        state.current_player = john
        state.players = [john, ai1, ai2]
        state.extra_card = None

        john._hand = [(5, 'L'), (9, 'H'), (6, '$')]
        ai1._hand = [(4, 'L'), (7, 'L'), (3, '$')]
        ai2._hand = [(1, 'L'), (3, 'H'), (5, '$')]

        accusation_cards = [(5, 'L'), (7, '$')]  # => murder card = 3H
        self.assertEqual(ai2, determine_murderer(state, accusation_cards))


if __name__ == '__main__':
    unittest.main()
