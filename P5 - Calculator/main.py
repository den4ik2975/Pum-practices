from transitions import Machine

from const import *
from calculator.lexer_machine import Automate
from calculator.main_class import Calculator


exp = input('Введи математическую формулу\n').replace(' ', '')

lexer = Automate()
machine = Machine(lexer, states=states, transitions=transitions, initial='start')

calc = Calculator(expression=exp, lexer=lexer)

calc.from_str_to_list()
calc.from_list_to_polska()

if calc.lexer.has_parameter is False:
    res = calc.from_polska_to_answer()
    print(res)
else:
    x1, x2 = map(float, input('Введите промежуток через пробел\n').split())
    m = input('Если хотите найти корень введите 1, если интеграл - 2\n')
    if m == '1':
        res = calc.from_func_to_answer(x1, x2)
    elif m == '2':
        res = calc.from_func_to_integral(x1, x2)
    print(res)