from algorithm import initial_state, create_mask, grover, probabilities_of, measure, count, most_frequent, qubits_for, count_solutions, iterations, run

read_array = lambda: tuple(input("Digite os valores do array: ").replace(",", " ").split())
read_target = lambda: input("Digite o target: ").strip()

array = read_array()
target = read_target()

n_qubits = qubits_for(len(array))
N = 2 ** n_qubits

target_expression = lambda x: x == target

state = initial_state(N)
mask = create_mask(array, target_expression, N)
M = count_solutions(mask)

if M == 0:
    print("Target não encontrado no array.")
else:
    k = iterations(N, M)

    final_state = run(state, grover(mask), k)

    probabilities = probabilities_of(final_state)
    results = measure(probabilities, 5)
    counts = count(results)
    solution = most_frequent(counts)

    print("Iteracoes:", k)
    print("Estado encontrado:", solution)
    print("Representacao binaria:",
          format(solution, f"0{n_qubits}b"))
    print("Valor no array:", array[solution])
    print("Probabilidade de sucesso:",
          f"{probabilities[solution] * 100:.2f}%")

    print("\nEvolucao por rodada:")
    print("\n".join(map(
        lambda r: f"  Rodada {r}: {probabilities_of(run(state, grover(mask), r))[solution] * 100:.2f}%",
        range(k + 1)
    )))

    print("\nMedicoes:", list(map(lambda r: format(r, f"0{n_qubits}b"), results)))
    print("\n".join(map(
        lambda item: f"  |{item[0]:0{n_qubits}b}> (valor {array[item[0]] if item[0] < len(array) else '-'}): {item[1]} vez(es)",
        sorted(counts.items(), key=lambda item: -item[1])
    )))

    print("\nDistribuicao de probabilidades:")

    print("\n".join(map(
        lambda item: (
            f"|{item[0]:0{n_qubits}b}>: {item[1] * 100:.2f}%"
        ),
        enumerate(probabilities)
    )))