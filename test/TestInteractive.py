import unittest

from Interactive import print_low_suit, print_secret, print_summary, ask_for
import Interactive
from Player import HumanPlayer
from TestUtils import captured_output


nb = 0


def output(stringio):
    return stringio.getvalue().strip()


class MyTestCase(unittest.TestCase):
    def test_print_low_suit(self):
        players = [HumanPlayer('john'), HumanPlayer('jim')]
        for player in players:
            player.set_low_suit('L')

        with captured_output() as (out, err):
            print_low_suit(players)

        self.assertEqual('Low Suits: [john: L] [jim: L]', output(out))

    def test_print_secret(self):
        players = [HumanPlayer('john'), HumanPlayer('jim')]
        players[1]._secret = 0

        with captured_output() as (out, err):
            print_secret(players)

        self.assertEqual('Secret to play: [john: 1] [jim: 0]', output(out))

    def test_print_summary_at_start(self):
        human = HumanPlayer('john')
        human._hand = [(3, 'L'), (5, 'H'), (9, '$')]

        with captured_output() as (out, err):
            print_summary(human, [human], extra_card=None)

        self.assertEqual('Game Summary\nYour hand: 3L 5H 9$\nSecret to play: [john: 1]', output(out))

    def test_print_summary_with_extra_card_and_low_suit(self):
        human = HumanPlayer('john')
        human._hand = [(3, 'L'), (5, 'H'), (9, '$')]
        human.set_low_suit('H')

        with captured_output() as (out, err):
            print_summary(human, [human], extra_card=(5, 'L'))

        self.assertEqual(
            'Game Summary\nYour hand: 3L 5H 9$\nExtra card: 5L\nLow Suits: [john: H]\nSecret to play: [john: 1]',
            output(out))

    def test_ask_for(self):
        try:
            old_raw_input = raw_input
            Interactive.raw_input = lambda _: 'test'

            self.assertEqual(u'test', ask_for('what?'))
        finally:
            Interactive.raw_input = old_raw_input

    def test_ask_for_with_control(self):
        def temp_raw_input(_):
            global nb
            if nb == 1:
                nb += 1
                return 'x'
            else:
                return 'a'

        try:
            global nb
            nb = 1
            old_raw_input = raw_input
            Interactive.raw_input = temp_raw_input

            with captured_output() as (out, err):
                response = ask_for('a or b ?', unicode, ['a', 'b'])

            self.assertEqual(u'a', response)
            self.assertEqual('> Invalid answer (allowed : a/b)', output(out))
        finally:
            Interactive.raw_input = old_raw_input

    def test_ask_for_with_cast(self):
        try:
            old_raw_input = raw_input
            Interactive.raw_input = lambda _: '123'

            self.assertEqual(123, ask_for('what?', wanted_type=int))
        finally:
            Interactive.raw_input = old_raw_input

if __name__ == '__main__':
    unittest.main()
