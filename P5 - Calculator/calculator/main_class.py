from calculator.lexer_machine import Automate
from calculator.polska_operations import translator, answer_totalizer
from calculator.root_and_integral import finder, integral_finder


class Calculator:
    def __init__(self, expression: str, lexer: Automate):
        self.expression = expression
        self.lexer = lexer
        self.list_result = []
        self.polska_result = []
        self.result = []
        self.answer = 0

    def from_str_to_list(self):
        self.list_result = self.lexer.start_analysis(self.expression)

    def from_list_to_polska(self):
        self.polska_result = translator(self.list_result)

    def from_polska_to_answer(self):
        self.result = answer_totalizer(self.polska_result)
        return self.result

    def from_func_to_answer(self, x1: float, x2: float):
        self.answer = finder(self.polska_result, x1, x2)
        return self.answer

    def from_func_to_integral(self, x1: float, x2: float):
        self.answer = integral_finder(self.polska_result, x1, x2)
        return self.answer

