from calculator.polska_operations import answer_totalizer


def f(x: float, func: list) -> float:
    func = [i if i != 'x' else str(x) for i in func]
    result = answer_totalizer(func)
    return result


def simpson_method(x1: float, x2: float, func: list) -> float:
    res = ((x2 - x1) / 6) * (f(x1, func) + 4 * f((x1 + x2) / 2, func) + f(x2, func))
    return res


def finder(func: list, x1: float, x2: float):  # func это функция в польской записи
    iterations = 90

    for i in range(iterations):
        y1 = f(x1, func)
        y2 = f(x2, func)
        if y1 * y2 > 0:
            return 'Невозможно определить корни'

        else:
            k = (y1 - y2) / (x1 - x2)
            b = y2 - k * x2

            new_x = -(b / k)
            new_y = f(new_x, func)

            if new_y * y1 > 0:
                x1 = new_x
            else:
                x2 = new_x

    return new_x


def integral_finder(func: list, x1: float, x2: float, iterations = 50000) -> float:
    step = (x2 - x1) / iterations
    current_step = x1
    summ = 0

    for i in range(iterations):
        next_step = current_step + step
        summ += simpson_method(current_step, next_step, func)
        current_step = next_step

    return summ

