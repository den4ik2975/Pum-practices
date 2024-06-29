from transitions import State
import math

transitions = [
    {'trigger': 'number', 'source': 'start', 'dest': 'integer', 'conditions': 'is_number'},
    {'trigger': 'next_number', 'source': 'integer', 'dest': '=', 'conditions': 'is_number'},
    {'trigger': 'close_bracket', 'source': ['integer', 'floating', 'parameter'], 'dest': 'bracket', 'conditions': 'is_close_bracket'},
    {'trigger': 'next_close_bracket', 'source': 'bracket', 'dest': '=', 'conditions': 'is_close_bracket'},
    {'trigger': 'dot', 'source': 'integer', 'dest': 'floating', 'conditions': 'is_dot'},
    {'trigger': 'next_float', 'source': 'floating', 'dest': '=', 'conditions': 'is_number'},
    {'trigger': 'open_bracket', 'source': 'start', 'dest': '=', 'conditions': 'is_open_bracket'}, #with unary minus
    {'trigger': 'symbol', 'source': 'start', 'dest': 'func', 'conditions': 'is_symbol'}, #without x
    {'trigger': 'next_symbol', 'source': 'func', 'dest': None, 'conditions': 'is_next_symbol'},
    {'trigger': 'func_open_bracket', 'source': 'func', 'dest': 'start', 'conditions': 'is_open_bracket'},
    {'trigger': 'param', 'source': 'start', 'dest': 'parameter', 'conditions': 'is_param'}, #x
    {'trigger': 'operand', 'source': ['integer', 'floating', 'bracket', 'parameter'], 'dest': 'start', 'conditions': 'is_operand'},
]

states = [
    State(name='start', on_enter='add_piece'),
    State(name='integer'),
    State(name='bracket'),
    State(name='func', on_exit='check_name'),
    State(name='parameter'),
    State(name='floating')
]

priority = {
    '^': 3,
    'sin': 4,
    'cos': 4,
    'tg': 4,
    'ctg': 4,
    'ln': 4,
    'exp': 4,
    '*': 2,
    '/': 2,
    '+': 1,
    '-': 1
}

operations = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y,
    '^': lambda x, y: pow(x, y),
    'sin': lambda x: math.sin(x),
    'cos': lambda x: math.cos(x),
    'tg': lambda x: math.tan(x),
    'ctg': lambda x: 1 / math.tan(x),
    'ln': lambda x: math.log(x),
    'exp': lambda x: math.exp(x)
}
