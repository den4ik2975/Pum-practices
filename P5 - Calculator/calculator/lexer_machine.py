from string import ascii_lowercase
from errors import IncorrectInput


class Automate(object):
    def __init__(self):
        self.expression = ''
        self.hlp = ''
        self.result = []
        self.bracket_counter = 0
        self.state_checker = {}
        self.has_parameter = False
        self.correct_counter = 0
        self.is_unary_minus = False

    def start_analysis(self, expression: str) -> list:
        self.expression = expression

        self.state_checker = {
            'start': [self.number, self.open_bracket, self.param, self.symbol],
            'integer': [self.next_number, self.close_bracket, self.dot, self.operand],
            'floating': [self.next_float, self.close_bracket, self.operand],
            'bracket': [self.next_close_bracket, self.operand],
            'func': [self.next_symbol, self.func_open_bracket],
            'parameter': [self.operand, self.close_bracket]
        }

        for sym in self.expression:
            old_state = self.state
            self.correct_counter = 0

            for fun in self.state_checker[str(self.state)]:
                fun(sym)
                new_state = self.state

                if old_state != new_state:
                    break

            if self.correct_counter != 1:
                raise IncorrectInput

        if self.bracket_counter != 0 or self.state in ['start', 'func']:
            print(self.bracket_counter)
            raise IncorrectInput

        self.add_piece()
        return self.result

    def check_name(self, val: str):
        if self.result[-1] not in ['sin', 'cos', 'tg', 'ctg', 'ln', 'exp']:
            raise IncorrectInput

    def add_piece(self, costyl=0):
        if self.hlp != '':
            if self.is_unary_minus is False:
                self.result += [self.hlp]
                self.hlp = ''
            else:
                self.is_unary_minus = False

    def is_number(self, val: str):
        if val.isdigit():
            self.hlp += val

            self.correct_counter += 1
            return True
        return False

    def is_dot(self, val: str):
        if val == '.':
            self.hlp += val

            self.correct_counter += 1
            return True
        return False

    def is_close_bracket(self, val: str):
        if val == ')':
            self.add_piece()
            self.hlp += val

            self.bracket_counter -= 1
            if self.bracket_counter < 0:
                raise IncorrectInput

            self.correct_counter += 1
            return True
        return False

    def is_open_bracket(self, val: str):
        if val == '(':
            self.add_piece()
            self.hlp += val
            self.bracket_counter += 1

            self.correct_counter += 1
            return True

        if val == '-':
            self.add_piece()
            self.hlp += val
            self.is_unary_minus = True

            self.correct_counter += 1
            return True
        return False

    def is_symbol(self, val: str):
        if val in ascii_lowercase and val != 'x':
            self.hlp += val
            self.correct_counter += 1
            return True
        return False

    def is_next_symbol(self, val: str):
        if val in ascii_lowercase:
            self.hlp += val
            self.correct_counter += 1
            return True
        return False

    def is_param(self, val: str):
        if val == 'x':
            self.hlp += val
            self.has_parameter = True
            self.correct_counter += 1
            return True
        return False

    def is_operand(self, val: str):
        if val in '-+*^/':
            self.add_piece()
            self.hlp += val
            self.correct_counter += 1
            return True
        return False