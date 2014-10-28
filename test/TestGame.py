import unittest
from Game import prepare_game_deck


class MyTestCase(unittest.TestCase):
    def test_prepare_game_deck(self):
        self.assertEqual(3 * 9 * 3, len(prepare_game_deck(3)))


if __name__ == '__main__':
    unittest.main()
