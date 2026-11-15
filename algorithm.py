import numpy as np
from functools import reduce
from math import sqrt, asin, pi

n_qubits = 3
N = 2 ** n_qubits
target = 5

target_expression = lambda x: x == target

state = np.full(N, 1 / sqrt(N), dtype=complex)

mascara = np.fromiter(
    map(target_expression, range(N)),
    dtype=bool,
    count=N
)

oracle = lambda state: np.where(
    mascara, -state, state
)

diffuser = lambda state: (
    2 * np.mean(state) - state
)

grover = lambda state: diffuser(oracle(state))

M = sum(map(target_expression, range(N)))

theta = asin(sqrt(M / N))
k = round(pi / (4 * theta) - 0.5)

final_state = reduce(
    lambda atual, _: grover(atual),
    range(k),
    state
)

probabilities = np.abs(final_state) ** 2
solution = np.argmax(probabilities)

print("Iteracoes:", k)
print("Estado encontrado:", solution)
print("Representacao binaria:",
      format(solution, f"0{n_qubits}b"))
print("Probabilidade de sucesso:",
      f"{probabilities[solution] * 100:.2f}%")

print("\nDistribuicao de probabilidades:")

print("\n".join(map(
    lambda item: (
        f"|{item[0]:0{n_qubits}b}>: {item[1] * 100:.2f}%"
    ),
    enumerate(probabilities)
)))
