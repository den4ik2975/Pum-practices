import re
from const import operations
from const import priority


def answer_totalizer(polska_list: list) -> float:

    stack = []
    for i in polska_list:
        if re.match('[-+]?[0-9]+[.]*[0-9]*', i):
            stack.append(i)

        elif i in ['+', '-', '*', '/', '^']:
            otv = operations[i](float(stack[-2]), float(stack[-1]))

            del stack[-2:]
            stack += [otv]

        else:
            otv = operations[i](float(stack[-1]))

            del stack[-1:]
            stack += [otv]

    return stack[0]


def translator(code: list) -> list:
    texas = []
    result = []

    for v in code:

        if re.match('[-+]?[0-9]+[.]*[0-9]*', v) or v == 'x':
            result.append(v)

        elif v in priority:
            while len(texas) > 0 and texas[-1] != '(' and priority[v] <= priority[texas[-1]]:
                result.append(texas.pop())

            texas.append(v)

        elif v == ')':
            while len(texas) > 0:
                x = texas.pop()
                if x == '(':
                    break
                result.append(x)

        elif v == '(':
            texas.append(v)

    while len(texas) > 0:
        result.append(texas.pop())

    return result
