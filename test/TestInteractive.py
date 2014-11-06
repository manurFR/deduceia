import unittest
from Deck import Range

from GameState import GameState
from Interactive import print_low_suit, print_secret, print_summary, ask_for, quit_command, interrogate_command, \
    print_question_cards, choose_an_opponent, maxlength_by_column, print_tabular_data, print_history, secret_command, \
    HIDDEN, accuse_command
import Interactive
from Player import HumanPlayer, AIPlayer
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

        self.assertEqual('Game Summary\n'
                         'Your hand: 3L 5H 9$\n'
                         'Secret to play: [john: 1]', output(out))

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
            'Game Summary\n'
            'Your hand: 3L 5H 9$\n'
            'Extra card: 5L\n'
            'Low Suits: [john: H]\n'
            'Secret to play: [john: 1]',
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

    def test_choose_an_opponent(self):
        try:
            old_raw_input = raw_input
            Interactive.raw_input = mock_raw_input('5', '2')

            player = HumanPlayer('joe')
            ai1 = AIPlayer(1)
            ai2 = AIPlayer(2)
            ai3 = AIPlayer(3)

            state = GameState()
            state.turn = 1
            state.current_player = player
            state.players = [ai2, player, ai3, ai1]

            with captured_output() as (out, err):
                chosen_opponent = choose_an_opponent(state)

            self.assertEqual(ai2, chosen_opponent)
        finally:
            Interactive.raw_input = old_raw_input

    def test_interrogate_asks_for_two_cards_puts_the_range_in_history_and_display_the_result(self):
        try:
            old_raw_input = raw_input
            Interactive.raw_input = mock_raw_input('1', '3L', '7L')  # opponent id, low card, high card

            player = HumanPlayer('joe')
            ai = AIPlayer(1)
            ai._hand = [(1, 'L'), (3, 'L'), (6, 'L'), (2, 'H'), (8, '$'), (9, '$')]

            state = GameState()
            state.turn = 10
            state.current_player = player
            state.players = [player, ai]
            state.question_cards = [(1, 'L'), (3, 'L'), (7, 'L')]

            with captured_output() as (out, err):
                turn_ended = interrogate_command(state)

            self.assertEqual('Interrogate\n'
                             'Question cards: 1L 3L 7L\n'
                             'Cards in this range: 2', output(out))
            turn = state.history.pop()
            self.assertEqual(10, turn['turn'])
            self.assertEqual('joe', turn['player'].name)
            self.assertEqual('AI#1', turn['opponent'].name)
            self.assertEqual('interrogate', turn['action'])
            self.assertEqual(['L'], turn['range'].suits)
            self.assertEqual([3, 4, 5, 6, 7], turn['range'].ranks)
            self.assertEqual(2, turn['result'])
            self.assertTrue(turn_ended)
        finally:
            Interactive.raw_input = old_raw_input

    def test_interrogate_lets_you_cancel_and_do_nothing(self):
        try:
            old_raw_input = raw_input
            Interactive.raw_input = mock_raw_input('1', '3L', 'cancel')

            player = HumanPlayer('joe')
            ai = AIPlayer(1)

            state = GameState()
            state.current_player = player
            state.players = [player, ai]
            state.history = []
            state.question_cards = [(1, 'L'), (3, 'L'), (7, 'L')]

            with captured_output() as (out, err):
                turn_ended = interrogate_command(state)

            self.assertEqual('Interrogate\n'
                             'Question cards: 1L 3L 7L', output(out))
            self.assertEqual(0, len(state.history))
            self.assertFalse(turn_ended)
        finally:
            Interactive.raw_input = old_raw_input

    def test_interrogate_for_the_same_two_cards_asks_for_rank_or_suit(self):
        try:
            old_raw_input = raw_input
            Interactive.raw_input = mock_raw_input('1', '3L', '3L', 'suit')  # opponent id, low card, high card

            player = HumanPlayer('joe')
            ai = AIPlayer(1)
            ai._hand = [(1, 'L'), (3, 'L'), (6, 'L'), (2, 'H'), (8, '$'), (9, '$')]

            state = GameState()
            state.turn = 10
            state.current_player = player
            state.players = [player, ai]
            state.question_cards = [(1, '$'), (3, 'L'), (3, 'L')]

            with captured_output() as (out, err):
                turn_ended = interrogate_command(state)

            self.assertEqual('Interrogate\n'
                             'Question cards: 1$ 3L 3L\n'
                             'Cards in this range: 3', output(out))
            turn = state.history.pop()
            self.assertEqual(10, turn['turn'])
            self.assertEqual('joe', turn['player'].name)
            self.assertEqual('AI#1', turn['opponent'].name)
            self.assertEqual('interrogate', turn['action'])
            self.assertEqual('3L->3L [suit]', str(turn['range']))
            self.assertEqual(3, turn['result'])
            self.assertTrue(turn_ended)
        finally:
            Interactive.raw_input = old_raw_input

    def test_maxlength_by_column(self):
        data = [{'col1': 'hello', 'col2': 'a',      'col3': 4444,  'col4': 'z',    'col5': 'abcd'},
                {'col1': 'you',   'col2': 'column', 'col3': 55555, 'col4': HIDDEN, 'col5': 'efg'}]

        self.assertEqual([5, 5, 6, 4], maxlength_by_column(data, ['col1', 'col3', 'col2', 'col4']))

    def test_maxlength_by_column_no_headers(self):
        data = [{'header1': 'hello', 'header2': 'a'},
                {'header1': 'you',   'header2': 'column'}]

        self.assertEqual([5, 6], maxlength_by_column(data, ['header1', 'header2'], headers=False))

    def test_print_tabular_data(self):
        data = [{'col1': 'hello', 'col2': 'a',      'col3': 4444,  'col4': 'z'},
                {'col1': 'you',   'col2': 'column', 'col3': 55555, 'col4': HIDDEN}]

        with captured_output() as (out, err):
            print_tabular_data(data, ['col1', 'col3', 'col2', 'col4'], [5, 5,6, 4])

        self.assertEqual('Col1   Col3   Col2    Col4\n'
                         'hello  4444   a       z   \n'
                         'you    55555  column  ****',
                         output(out))

    def test_print_tabular_data_no_header(self):
        data = [{'header1': 'hello', 'header2': 'a'},
                {'header1': 'you',   'header2': 'column'}]

        with captured_output() as (out, err):
            print_tabular_data(data, ['header1', 'header2'], [5, 6], headers=False)

        self.assertEqual('hello  a     \n'
                         'you    column',
                         output(out))

    def test_print_history(self):
        tom = HumanPlayer('Tom')
        juanpedro = HumanPlayer('Juan-Pedro')
        joe = HumanPlayer('Joe')
        history = [{'turn': 1, 'player': tom, 'opponent': juanpedro,
                    'range': Range((1, 'L'), (5, 'L')), 'result': 2, 'action': 'interrogate'},
                   {'turn': 2, 'player': joe, 'opponent': tom,
                    'range': Range((6, '$'), (6, '$'), choice='suit'), 'result': 0, 'action': 'interrogate'},
                   {'turn': 3, 'player': juanpedro, 'opponent': tom,
                    'range': Range((3, 'L'), (3, 'H')), 'result': 1, 'action': 'secret'},
                   {'turn': 4, 'player': tom, 'opponent': juanpedro,
                    'range': Range((4, '$'), (7, '$')), 'result': 0, 'action': 'secret'},
                   {'turn': 5, 'player': joe, 'opponent': tom,
                    'range': Range((9, 'H'), (3, 'H')), 'result': 4, 'action': 'secret'}]
        accusations = [{'player': tom, 'accused': juanpedro, 'cards': [(8, 'H'), (3, '$')], 'outcome': 'incorrect'},
                       {'player': juanpedro, 'accused': joe, 'cards': [(7, 'H'), (5, '$')], 'outcome': 'correct'}]

        state = GameState()
        state.history = history
        state.accusations = accusations
        state.current_player = juanpedro

        with captured_output() as (out, err):
            self.assertFalse(print_history(state))

        self.assertEqual('History\n'
                         'Turn  Player      Opponent    Range          Result  Note    \n'
                         '1     Tom         Juan-Pedro  1L->5L         2               \n'
                         '2     Joe         Tom         6$->6$ [suit]  0               \n'
                         '3     Juan-Pedro  Tom         3L->3H         1       (Secret)\n'
                         '4     Tom         Juan-Pedro  4$->7$         0       (Secret)\n'
                         '5     Joe         Tom         *************  ******  (Secret)\n'
                         '\n'
                         'Accusations\n'
                         '      Tom         Juan-Pedro  8H 3$          incorrect\n'
                         '      Juan-Pedro  Joe         7H 5$          correct',
                         output(out))

    def test_secret_asks_for_two_cards_puts_the_range_in_history_and_display_the_result(self):
        try:
            old_raw_input = raw_input
            Interactive.raw_input = mock_raw_input('1', '9$', '1H')  # opponent id, low card, high card

            player = HumanPlayer('joe')
            ai = AIPlayer(1)
            ai._hand = [(1, 'L'), (3, 'L'), (6, 'L'), (2, 'H'), (8, '$'), (9, '$')]

            state = GameState()
            state.turn = 1
            state.current_player = player
            state.players = [player, ai]
            state.question_cards = [(1, 'L'), (3, 'L'), (7, 'L')]

            with captured_output() as (out, err):
                turn_ended = secret_command(state)

            self.assertEqual('Secret\n'
                             'Cards in this range: 2', output(out))
            turn = state.history.pop()
            self.assertEqual(1, turn['turn'])
            self.assertEqual('joe', turn['player'].name)
            self.assertEqual('AI#1', turn['opponent'].name)
            self.assertEqual('secret', turn['action'])
            self.assertEqual(['L', 'H', '$'], turn['range'].suits)
            self.assertEqual([9, 1], turn['range'].ranks)
            self.assertEqual(2, turn['result'])
            self.assertTrue(turn_ended)
        finally:
            Interactive.raw_input = old_raw_input

    def test_accuse_good_guess(self):
        try:
            old_raw_input = raw_input
            Interactive.raw_input = mock_raw_input('1', '5L', '5$')  # opponent id, first card, second card

            joe = HumanPlayer('joe')
            joe._hand = [(4, 'L'), (8, 'L'), (5, 'H'), (8, 'H')]
            ai = AIPlayer(1)
            ai._hand = [(1, 'L'), (3, 'L'), (1, 'H'), (9, '$')]

            state = GameState()
            state.turn = 23
            state.current_player = joe
            state.players = [joe, ai]
            state.evidence_cards = [(5, '$'), (5, 'L')]

            with captured_output() as (out, err):
                self.assertTrue(accuse_command(state))

            self.assertEqual('Accuse\n\n'
                             'Your guess is: Correct', output(out))
            accusation = state.accusations.pop()
            self.assertEqual('joe', accusation['player'].name)
            self.assertEqual('AI#1', accusation['accused'].name)
            self.assertEqual([(5, 'L'), (5, '$')], accusation['cards'])
            self.assertEqual('correct', accusation['outcome'])
        finally:
            Interactive.raw_input = old_raw_input

    def test_accuse_bad_guess_of_cards(self):
        try:
            old_raw_input = raw_input
            Interactive.raw_input = mock_raw_input('1', '1L', '2L')  # opponent id, first card, second card

            joe = HumanPlayer('joe')
            joe._hand = [(4, 'L'), (8, 'L'), (5, 'H'), (8, 'H')]
            ai = AIPlayer(1)
            ai._hand = [(1, 'L'), (3, 'L'), (1, 'H'), (9, '$')]

            state = GameState()
            state.turn = 23
            state.current_player = joe
            state.players = [joe, ai]
            state.evidence_cards = [(5, '$'), (5, 'L')]

            with captured_output() as (out, err):
                self.assertTrue(accuse_command(state))

            self.assertEqual('Accuse\n\n'
                             'Your guess is: Incorrect', output(out))
            accusation = state.accusations.pop()
            self.assertEqual('joe', accusation['player'].name)
            self.assertEqual('AI#1', accusation['accused'].name)
            self.assertEqual([(1, 'L'), (2, 'L')], accusation['cards'])
            self.assertEqual('incorrect', accusation['outcome'])
        finally:
            Interactive.raw_input = old_raw_input

    def test_accuse_bad_guess_of_murderer(self):
        try:
            old_raw_input = raw_input
            Interactive.raw_input = mock_raw_input('1', '3L', '5L')  # opponent id, first card, second card

            joe = HumanPlayer('joe')
            joe._hand = [(4, 'L'), (7, 'L'), (5, 'H'), (8, 'H')]
            ai1 = AIPlayer(1)
            ai1._hand = [(1, 'L'), (3, 'L'), (1, 'H'), (9, '$')]
            ai2 = AIPlayer(2)
            ai2._hand = [(8, 'L'), (3, 'H'), (2, '$'), (3, '$')]

            state = GameState()
            state.turn = 23
            state.current_player = joe
            state.players = [joe, ai1, ai2]
            state.evidence_cards = [(3, 'L'), (5, 'L')]

            with captured_output() as (out, err):
                self.assertTrue(accuse_command(state))

            self.assertEqual('Accuse\n\n'
                             'Your guess is: Incorrect', output(out))
        finally:
            Interactive.raw_input = old_raw_input

if __name__ == '__main__':
    unittest.main()

