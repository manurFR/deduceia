import unittest

from Deck import Range
from Sheet import Sheet
from TestUtils import sheet_table


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

        self.assertEqual(sheet_table(excluded=[(1, 'L'), (5, 'H'), (9, '$')]), sheet.table)

    def test_exclude_cards_with_only_one_card(self):
        sheet = Sheet('test')
        sheet.exclude_cards((8, '$'))

        self.assertEqual(sheet_table(excluded=[(8, '$')]), sheet.table)

    def test_own_cards(self):
        sheet = Sheet('test')
        sheet.own_cards([(3, 'L'), (3, 'H'), (3, '$')])

        self.assertEqual(sheet_table(owned=[(3, 'L'), (3, 'H'), (3, '$')]), sheet.table)

    def test_set_suit_total(self):
        sheet = Sheet('test')
        sheet.own_cards([(5, 'L')])
        sheet.set_suit_total('L', 3)

        self.assertEqual(sheet_table(owned=[(5, 'L')], totals={'L': 3}), sheet.table)

    def test_voids(self):
        sheet = Sheet('test')
        sheet.exclude_cards(Range((2, 'L'), (8, '$')).cards())

        self.assertItemsEqual([(1, 'L'), (1, 'H'), (1, '$'), (9, 'L'), (9, 'H'), (9, '$')], sheet.voids())

    def test_voids_for_a_suit(self):
        sheet = Sheet('test')
        sheet.exclude_cards(Range((2, 'L'), (8, '$')).cards())

        self.assertItemsEqual([(1, 'H'), (9, 'H')], sheet.voids('H'))

    def test_owned(self):
        sheet = Sheet('test')
        sheet.own_cards([(2, 'L'), (6, 'L'), (3, 'H')])

        self.assertItemsEqual([(2, 'L'), (6, 'L'), (3, 'H')], sheet.owned())

    def test_owned_for_a_suit(self):
        sheet = Sheet('test')
        sheet.own_cards([(2, 'L'), (6, 'L'), (3, 'H')])

        self.assertItemsEqual([(2, 'L'), (6, 'L')], sheet.owned('L'))

    def test_exclude_when_void_marks_unknown_cards_as_excluded(self):
        sheet = Sheet('test')
        sheet.own_cards([(2, 'L'), (6, 'L'), (9, 'L')])

        sheet.exclude_when_void('L')

        self.assertEqual(sheet_table(excluded=[(1, 'L'), (3, 'L'), (4, 'L'), (5, 'L'), (7, 'L'), (8, 'L')],
                                     owned=[(2, 'L'), (6, 'L'), (9, 'L')]),
                         sheet.table)

    def test_own_when_void_marks_unknown_cards_as_owned(self):
        sheet = Sheet('test')
        sheet.exclude_cards([(2, 'L'), (6, 'L'), (9, 'L')])

        sheet.own_when_void('L')

        self.assertEqual(sheet_table(excluded=[(2, 'L'), (6, 'L'), (9, 'L')],
                                     owned=[(1, 'L'), (3, 'L'), (4, 'L'), (5, 'L'), (7, 'L'), (8, 'L')]),
                         sheet.table)


if __name__ == '__main__':
    unittest.main()
