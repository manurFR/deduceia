import unittest
from Sheet import Sheet


class TestSheet(unittest.TestCase):
    def test_init(self):
        sheet = Sheet('test')

        self.assertEqual('test', sheet.subject)
        self.assertEqual(-1, sheet.grand_total)
        self.assertEqual(
            {'L': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1, 'total': -1},
             'H': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1, 'total': -1},
             '$': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1, 'total': -1},
             'total': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1}}, sheet.table)

    def test_exclude_cards(self):
        sheet = Sheet('test')
        sheet.exclude_cards([(1, 'L'), (5, 'H'), (9, '$')])

        self.assertEqual(
            {'L': {1:  0, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1, 'total': -1},
             'H': {1: -1, 2: -1, 3: -1, 4: -1, 5:  0, 6: -1, 7: -1, 8: -1, 9: -1, 'total': -1},
             '$': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9:  0, 'total': -1},
             'total': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1}}, sheet.table)

    def test_exclude_cards_with_only_one_card(self):
        sheet = Sheet('test')
        sheet.exclude_cards((8, '$'))

        self.assertEqual(
            {'L': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1, 'total': -1},
             'H': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1, 'total': -1},
             '$': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8:  0, 9: -1, 'total': -1},
             'total': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1}}, sheet.table)

    def test_own_cards(self):
        sheet = Sheet('test')
        sheet.own_cards([(3, 'L'), (3, 'H'), (3, '$')])

        self.assertEqual(
            {'L': {1: -1, 2: -1, 3:  1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1, 'total': -1},
             'H': {1: -1, 2: -1, 3:  1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1, 'total': -1},
             '$': {1: -1, 2: -1, 3:  1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1, 'total': -1},
             'total': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1}}, sheet.table)


if __name__ == '__main__':
    unittest.main()
