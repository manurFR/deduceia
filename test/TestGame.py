import unittest

from Game import prepare_game_deck, prepare_players
from Player import HumanPlayer


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
        self.assertEqual(1, [player.name for player in players].count('Test'))


if __name__ == '__main__':
    unittest.main()
