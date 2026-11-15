import numpy as np

from math import sqrt, asin, pi
from functools import reduce
from collections.abc import Callable

def number_of_states(n_qubits: int) -> int:

    if n_qubits < 1:
        raise ValueError("É necessário pelo menos um qubit.")

    return 2 ** n_qubits


def create_uniform_state(n_qubits: int) -> np.ndarray:

    n_states = number_of_states(n_qubits)

    amplitude = 1 / sqrt(n_states)

    return np.full(
        n_states,
        amplitude,
        dtype=np.complex128
    )


def is_solution(x: int) -> bool:

    return x == 5


def count_solutions(
    n_states: int,
    predicate: Callable[[int], bool]
) -> int:

    return sum(map(predicate, range(n_states)))


def phase_oracle(
    state: np.ndarray,
    predicate: Callable[[int], bool]
) -> np.ndarray:

    mask = np.fromiter(
        map(predicate, range(state.size)),
        dtype=bool,
        count=state.size
    )

    return np.where(mask, -state, state)


def diffuser(state: np.ndarray) -> np.ndarray:

    mean_amplitude = np.mean(state)

    return 2 * mean_amplitude - state


def grover_iteration(
    state: np.ndarray,
    predicate: Callable[[int], bool]
) -> np.ndarray:

    return diffuser(
        phase_oracle(state, predicate)
    )


def optimal_iterations(
    n_states: int,
    n_solutions: int
) -> int:

    if not 0 < n_solutions <= n_states:
        raise ValueError("Quantidade inválida de soluções.")

    theta = asin(sqrt(n_solutions / n_states))

    return max(0, round(pi / (4 * theta) - 0.5))


def run_grover(
    n_qubits: int,
    predicate: Callable[[int], bool],
    iterations: int | None = None
) -> np.ndarray:

    n_states = number_of_states(n_qubits)

    n_solutions = count_solutions(n_states, predicate)

    if n_solutions == 0:
        raise ValueError("Nenhuma solução encontrada.")

    if iterations is None:
        iterations = optimal_iterations(
            n_states,
            n_solutions
        )

    if not isinstance(iterations, int) or iterations < 0:
        raise ValueError("Número de iterações inválido.")

    initial_state = create_uniform_state(n_qubits)

    return reduce(
        lambda current_state, _: grover_iteration(
            current_state,
            predicate
        ),
        range(iterations),
        initial_state
    )


def probability_distribution(
    state: np.ndarray
) -> np.ndarray:

    probabilities = np.abs(state) ** 2

    return probabilities / probabilities.sum()


def most_likely_state(state: np.ndarray) -> int:

    probabilities = probability_distribution(state)

    return int(np.argmax(probabilities))


def measure_once(
    state: np.ndarray,
    seed: int = 42
) -> int:

    probabilities = probability_distribution(state)

    rng = np.random.default_rng(seed)

    return int(
        rng.choice(len(probabilities), p=probabilities)
    )


# EXECUÇÃO PRINCIPAL
if __name__ == "__main__":

    n_qubits = 3

    final_state = run_grover(
        n_qubits,
        is_solution
    )

    probabilities = probability_distribution(final_state)

    solution = most_likely_state(final_state)

    print("Número de iterações:",
          optimal_iterations(2 ** n_qubits, 1))

    print("\nEstado mais provável:", solution)

    print("Medição simulada:",
          format(measure_once(final_state), f"0{n_qubits}b"))
