import unittest
from GameState import GameState
from Player import HumanPlayer, AIPlayer


class MyTestCase(unittest.TestCase):
    def test_players_except(self):
        state = GameState()
        tom = HumanPlayer('tom')
        tim = AIPlayer('tim')
        tam = AIPlayer('tam')
        ari = AIPlayer('ari')

        state.players = [tom, tim, tam, ari]

        self.assertEqual([tom, tam], state.players_except(tim, ari))

    def test_players_except_should_return_gracefully_if_player_not_in_players(self):
        state = GameState()
        tom = HumanPlayer('tom')
        tim = AIPlayer('tim')

        state.players = [tom]

        try:
            self.assertEqual([tom], state.players_except(tim))
        except ValueError:
            self.fail("GameState.players_except(person) should not fail if person is not in players")

if __name__ == '__main__':
    unittest.main()
