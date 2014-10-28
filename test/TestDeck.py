import unittest
from Deck import prepare_deck, resolve_murder_card


class MyTestCase(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()
