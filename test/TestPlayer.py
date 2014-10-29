import unittest
from Player import HumanPlayer


class TestPlayer(unittest.TestCase):
    def test_hand_is_sorted(self):
        player = HumanPlayer('test')
        for card in [(2, '$'), (9, 'L'), (8, 'H'), (2, 'H'), (4, 'L')]:
            player.deal_card(card)

        self.assertEqual([(4, 'L'), (9, 'L'), (2, 'H'), (8, 'H'), (2, '$')], player.hand)


if __name__ == '__main__':
    unittest.main()
