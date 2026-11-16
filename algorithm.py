from functools import reduce
from math import asin, sqrt, pi

soma = lambda values: reduce(lambda aux, x: aux + x, values, 0)
media = lambda values: soma(values) / len(values)

initial_state = lambda N: tuple(map(lambda _: 1 / sqrt(N), range(N)))
create_mask = lambda array, target_expression, N: tuple(
    map(lambda i: i < len(array) and target_expression(array[i]), range(N))
)
oracle = lambda mask: lambda state: tuple(
    map(lambda pair: -pair[1] if pair[0] else pair[1], zip(mask, state))
)
diffuser = lambda state: (lambda m: tuple(map(lambda a: 2 * m - a, state)))(media(state))
grover = lambda mask: lambda state: diffuser(oracle(mask)(state))
probabilities_of = lambda state: tuple(map(lambda a: abs(a) ** 2, state))
argmax = lambda values: reduce(
    lambda best, i: i if values[i] > values[best] else best, range(len(values)), 0
)

qubits_for = lambda size: max(2, (size - 1).bit_length())

count_solutions = lambda mask: soma(map(int, mask))

iterations = lambda N, M: round(pi / (4 * asin(sqrt(M / N))) - 0.5)

run = lambda state, step, k: reduce(lambda atual, _: step(atual), range(k), state)