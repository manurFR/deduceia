import unittest

from GameState import GameState
from Interactive import print_low_suit, print_secret, print_summary, ask_for, quit_command, interrogate_command, \
    print_question_cards
import Interactive
from Player import HumanPlayer
from TestUtils import captured_output


def output(stringio):
    return stringio.getvalue().strip()


def mock_raw_input(*inputs):
    def temp_raw_input(_):
        global index_of_prompt
        try:
            reponse = inputs[index_of_prompt]
        except IndexError:
            raise AssertionError("mock_raw_input() was asked for too much input")
        index_of_prompt += 1
        return reponse
    global index_of_prompt
    index_of_prompt = 0
    return temp_raw_input

# noinspection PyUnboundLocalVariable
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

    def test_print_question_cards(self):
        state = GameState
        state.question_cards = [(3, 'L'), (3, 'H'), (6, '$')]

        with captured_output() as (out, err):
            print_question_cards(state)

        self.assertEqual('Question cards: 3L 3H 6$', output(out))


    def test_print_summary_at_start(self):
        human = HumanPlayer('john')
        human._hand = [(3, 'L'), (5, 'H'), (9, '$')]

        state = GameState()
        state.human_player = human
        state.players = [human]

        with captured_output() as (out, err):
            print_summary(state)

        self.assertEqual('Game Summary\nYour hand: 3L 5H 9$\nSecret to play: [john: 1]', output(out))

    def test_print_summary_with_extra_card_and_low_suit(self):
        human = HumanPlayer('john')
        human._hand = [(3, 'L'), (5, 'H'), (9, '$')]
        human.set_low_suit('H')

        state = GameState()
        state.human_player = human
        state.players = [human]
        state.extra_card = (5, 'L')

        with captured_output() as (out, err):
            self.assertFalse(print_summary(state))

        self.assertEqual(
            'Game Summary\nYour hand: 3L 5H 9$\nExtra card: 5L\nLow Suits: [john: H]\nSecret to play: [john: 1]',
            output(out))

    def test_ask_for(self):
        try:
            old_raw_input = raw_input
            Interactive.raw_input = mock_raw_input('test')

            self.assertEqual(u'test', ask_for('what?'))
        finally:
            Interactive.raw_input = old_raw_input

    def test_ask_for_with_control(self):
        try:
            old_raw_input = raw_input
            Interactive.raw_input = mock_raw_input('invalid response', 'a')

            with captured_output() as (out, err):
                response = ask_for('a or b ?', unicode, ['a', 'b'])

            self.assertEqual(u'a', response)
            self.assertEqual('> Invalid answer (allowed : a/b)', output(out))
        finally:
            Interactive.raw_input = old_raw_input

    def test_ask_for_with_cast(self):
        try:
            old_raw_input = raw_input
            Interactive.raw_input = mock_raw_input('123')

            self.assertEqual(123, ask_for('what?', wanted_type=int))
        finally:
            Interactive.raw_input = old_raw_input

    def test_quit_but_dont_confirm(self):
        try:
            old_raw_input = raw_input
            Interactive.raw_input = mock_raw_input('n')

            self.assertEqual(False, quit_command(None))
        except SystemExit:
            self.fail("Should not exit in this case")
        finally:
            Interactive.raw_input = old_raw_input

    def test_quit_and_confirm(self):
        try:
            old_raw_input = raw_input
            Interactive.raw_input = mock_raw_input('y')

            with captured_output() as (out, err):
                quit_command(None)

            self.fail("Should exit in this case")
        except SystemExit:
            self.assertEqual("Bye.", output(out))
        finally:
            Interactive.raw_input = old_raw_input

    def test_interrogate_asks_for_two_cards_and_puts_the_range_in_history(self):
        try:
            old_raw_input = raw_input
            Interactive.raw_input = mock_raw_input('3L', '7L')

            player = HumanPlayer('joe')

            state = GameState()
            state.turn = 10
            state.current_player = player
            state.question_cards = [(1, 'L'), (3, 'L'), (7, 'L')]

            with captured_output() as (out, err):
                turn_ended = interrogate_command(state)

            self.assertEqual('Interrogate\nQuestion cards: 1L 3L 7L', output(out))
            turn = state.history.pop()
            self.assertEqual(10, turn['turn'])
            self.assertEqual(player, turn['player'])
            self.assertEqual('interrogate', turn['action'])
            self.assertEqual(['L'], turn['range'].suits)
            self.assertEqual([3, 4, 5, 6, 7], turn['range'].ranks)
            self.assertTrue(turn_ended)
        finally:
            Interactive.raw_input = old_raw_input

    def test_interrogate_lets_you_cancel_and_do_nothing(self):
        try:
            old_raw_input = raw_input
            Interactive.raw_input = mock_raw_input('3L', 'cancel')

            state = GameState()
            state.history = []
            state.question_cards = [(1, 'L'), (3, 'L'), (7, 'L')]

            with captured_output() as (out, err):
                turn_ended = interrogate_command(state)

            self.assertEqual('Interrogate\nQuestion cards: 1L 3L 7L', output(out))
            self.assertEqual(0, len(state.history))
            self.assertFalse(turn_ended)
        finally:
            Interactive.raw_input = old_raw_input


if __name__ == '__main__':
    unittest.main()
