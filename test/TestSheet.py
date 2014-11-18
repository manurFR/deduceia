import unittest
from Sheet import Sheet


class TestSheet(unittest.TestCase):
    def test_init(self):
        sheet = Sheet('test')

        self.assertEqual('test', sheet.subject)
        self.assertEqual(-1, sheet.grand_total)
        self.assertEqual(
            {'$':     {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1, 'total': -1},
             'H':     {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1, 'total': -1},
             'L':     {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1, 'total': -1},
             'total': {1: -1, 2: -1, 3: -1, 4: -1, 5: -1, 6: -1, 7: -1, 8: -1, 9: -1}}, sheet.table)


if __name__ == '__main__':
    unittest.main()
