import random
from functools import reduce
from math import asin, sqrt, pi

# Medição: sorteia a saída, cada número com sua probabilidade
measure = lambda probabilities, shots: random.choices(
    range(len(probabilities)), weights=probabilities, k=shots
)

# Conta quantas vezes cada posição saiu nos sorteios.
count = lambda results: reduce(lambda aux, r: {**aux, r: aux.get(r, 0) + 1}, results, {})

# Posição que mais saiu nos sorteios.
most_frequent = lambda counts: max(counts, key=counts.get)

# Soma todos os valores usando reduce (acumula um por um).
soma = lambda values: reduce(lambda aux, x: aux + x, values, 0)

# Média: soma dos valores dividida pela quantidade.
media = lambda values: soma(values) / len(values)

# Superposição: N pesos iguais a 1/sqrt(N), todos os números com a mesma chance.
initial_state = lambda N: tuple(map(lambda _: 1 / sqrt(N), range(N)))

# Máscara: True nas posições do array que têm o target, False nas outras.
create_mask = lambda array, target_expression, N: tuple(
    map(lambda i: i < len(array) and target_expression(array[i]), range(N))
)

# Oráculo: troca o sinal do peso nas posições marcadas pela máscara.
oracle = lambda mask: lambda state: tuple(
    map(lambda pair: -pair[1] if pair[0] else pair[1], zip(mask, state))
)

# Difusor: cada peso vira 2 * média - peso, aumentando a chance do marcado.
diffuser = lambda state: (lambda m: tuple(map(lambda a: 2 * m - a, state)))(media(state))

# Uma rodada do Grover: oráculo seguido do difusor.
grover = lambda mask: lambda state: diffuser(oracle(mask)(state))

# Probabilidade de cada posição: peso ao quadrado.
probabilities_of = lambda state: tuple(map(lambda a: abs(a) ** 2, state))

# Posição com a maior probabilidade, usando reduce.
argmax = lambda values: reduce(
    lambda best, i: i if values[i] > values[best] else best, range(len(values)), 0
)

# Quantidade de qubits necessária para o tamanho do array (mínimo 2).
qubits_for = lambda size: max(2, (size - 1).bit_length())

# Quantas posições têm o target (soma dos True da máscara).
count_solutions = lambda mask: soma(map(int, mask))

# Número ideal de rodadas, calculado pelo ângulo inicial theta.
iterations = lambda N, M: round(pi / (4 * asin(sqrt(M / N))) - 0.5)

# Aplica a rodada do Grover k vezes, cada uma sobre o resultado da anterior.
run = lambda state, step, k: reduce(lambda atual, _: step(atual), range(k), state)