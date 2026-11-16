# Quantum Grover's Algorithm — Versão Funcional

Simulação clássica do **Algoritmo de Grover** escrita em Python puro e no estilo de **programação funcional**: sem classes, sem laços `for`/`while`, sem variáveis mutáveis e sem dependências externas (nem NumPy). Todo o algoritmo é composto por funções `lambda`, `map`, `reduce` e tuplas imutáveis.

---

## Sumário

- [O que é o Algoritmo de Grover](#o-que-é-o-algoritmo-de-grover)
- [Por que programação funcional](#por-que-programação-funcional)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Como executar](#como-executar)
- [Exemplo de uso](#exemplo-de-uso)
- [Como funciona](#como-funciona)
- [Referência das funções](#referência-das-funções)
- [Limitações](#limitações)
- [Licença](#licença)

---

## O que é o Algoritmo de Grover

O Algoritmo de Grover é um algoritmo quântico de busca em uma lista não ordenada. Classicamente, encontrar um elemento entre `N` posições exige, no pior caso, `O(N)` consultas. Grover encontra o elemento com alta probabilidade em aproximadamente:

```
O(√N) consultas
```

Ele faz isso partindo de uma **superposição uniforme** de todos os estados e aplicando repetidamente dois operadores:

1. **Oráculo** — inverte o sinal da amplitude dos estados que são solução.
2. **Difusor** (inversão sobre a média) — amplifica as amplitudes marcadas e reduz as demais.

Após o número ideal de iterações, uma **medição** retorna a solução com probabilidade próxima de 100%.

---

## Por que programação funcional

Esta implementação foi escrita para mostrar que o algoritmo pode ser expresso inteiramente como **composição de funções puras**:

| Princípio | Como aparece no código |
|---|---|
| **Imutabilidade** | Os estados quânticos são `tuple`s; cada operação devolve uma tupla nova. |
| **Funções puras** | `oracle`, `diffuser`, `grover`, `probabilities_of` etc. não têm efeitos colaterais. |
| **Funções de alta ordem** | `oracle(mask)` e `grover(mask)` retornam funções que recebem um estado. |
| **Sem laços imperativos** | Repetição feita com `map` e `reduce` (ex.: `run` aplica `k` rodadas via `reduce`). |
| **Composição** | Uma rodada de Grover é `diffuser ∘ oracle(mask)`. |
| **Sem dependências** | Apenas a biblioteca padrão: `random`, `functools.reduce` e `math`. |

O único ponto não determinístico é a **medição** (`measure`), que usa `random.choices` para simular o colapso do estado quântico.

---

## Estrutura do projeto

```
Quantum-Grover-s-Algorithm/
├── algorithm.py   # Núcleo do algoritmo: todas as funções puras (lambdas)
├── main.py        # Interface de linha de comando: lê a entrada e exibe os resultados
├── LICENSE        # Licença MIT
└── README.md
```

---

## Como executar

**Requisitos:** Python 3.8 ou superior. Nenhuma biblioteca externa é necessária.

```bash
git clone <url-do-repositorio>
cd Quantum-Grover-s-Algorithm
python main.py
```

O programa pede:

1. **Os valores do array** — separados por espaço ou vírgula.
2. **O target** — o valor a ser buscado.

---

## Exemplo de uso

```
Digite os valores do array: 3, 7, 1, 9, 4, 2
Digite o target: 9
Iteracoes: 2
Estado encontrado: 3
Representacao binaria: 011
Valor no array: 9
Probabilidade de sucesso: 94.53%

Evolucao por rodada:
  Rodada 0: 12.50%
  Rodada 1: 78.12%
  Rodada 2: 94.53%

Medicoes: ['011', '011', '011', '011', '011']
  |011> (valor 9): 5 vez(es)

Distribuicao de probabilidades:
|000>: 0.78%
|001>: 0.78%
|010>: 0.78%
|011>: 94.53%
|100>: 0.78%
|101>: 0.78%
|110>: 0.78%
|111>: 0.78%
```

Com 6 elementos, são usados 3 qubits (`N = 8` estados). Em apenas 2 rodadas, a probabilidade de medir o índice correto sobe de 12,5% para 94,53%.

---

## Como funciona

O fluxo em [main.py](main.py) segue as etapas do algoritmo:

```
entrada ─► qubits_for ─► initial_state ─► create_mask ─► iterations
                                                            │
             saída ◄── most_frequent ◄── count ◄── measure ◄┴─ run(grover(mask))
```

1. **Número de qubits** — `qubits_for(len(array))` calcula quantos qubits são necessários para indexar o array (mínimo 2). O espaço de busca tem `N = 2^n` estados.
2. **Superposição** — `initial_state(N)` cria `N` amplitudes iguais a `1/√N`.
3. **Máscara** — `create_mask` marca com `True` os índices cujo valor é igual ao target. Posições além do tamanho do array (preenchimento até `N`) ficam `False`.
4. **Número de soluções** — `count_solutions(mask)` conta quantos índices são solução (`M`). Se `M = 0`, o programa informa que o target não existe.
5. **Iterações ideais** — `iterations(N, M)` calcula:

   ```
   θ = arcsen(√(M/N))
   k = round(π / (4θ) − 1/2)
   ```

6. **Amplificação** — `run(state, grover(mask), k)` aplica `k` vezes a rodada de Grover:
   - **Oráculo:** `aᵢ → −aᵢ` se `i` é solução.
   - **Difusor:** `aᵢ → 2·média − aᵢ`.
7. **Medição** — `probabilities_of` eleva cada amplitude ao quadrado; `measure` sorteia 5 *shots* com esses pesos; `most_frequent` escolhe o resultado mais observado.

---

## Referência das funções

Todas definidas em [algorithm.py](algorithm.py):

| Função | Assinatura | Descrição |
|---|---|---|
| `initial_state` | `N → estado` | Superposição uniforme com `N` amplitudes `1/√N`. |
| `create_mask` | `(array, expr, N) → máscara` | Tupla de booleanos indicando os índices que satisfazem `expr`. |
| `oracle` | `máscara → (estado → estado)` | Inverte o sinal das amplitudes marcadas. |
| `diffuser` | `estado → estado` | Inversão sobre a média: `2·média − a`. |
| `grover` | `máscara → (estado → estado)` | Uma rodada: oráculo seguido do difusor. |
| `run` | `(estado, passo, k) → estado` | Aplica `passo` `k` vezes usando `reduce`. |
| `iterations` | `(N, M) → k` | Número ideal de rodadas. |
| `qubits_for` | `tamanho → n` | Quantidade de qubits necessária (mínimo 2). |
| `count_solutions` | `máscara → M` | Quantidade de soluções marcadas. |
| `probabilities_of` | `estado → probabilidades` | Quadrado do módulo de cada amplitude. |
| `measure` | `(probabilidades, shots) → resultados` | Simula medições com `random.choices`. |
| `count` | `resultados → dict` | Frequência de cada resultado (via `reduce`). |
| `most_frequent` | `dict → índice` | Resultado observado mais vezes. |
| `argmax` | `valores → índice` | Índice do maior valor (via `reduce`). |
| `soma` / `media` | `valores → número` | Soma e média implementadas com `reduce`. |

Como o critério de busca é uma função (`target_expression`), é fácil trocar a igualdade por qualquer outro predicado, por exemplo:

```python
target_expression = lambda x: int(x) > 5
```

---

## Limitações

- É uma **simulação clássica**: o vetor de estado ocupa memória `O(N)` e cada rodada custa `O(N)`, então não há ganho real de desempenho — o objetivo é didático.
- O espaço de busca cresce em potências de 2; arrays pequenos são completados com posições vazias.
- A medição é probabilística: em casos raros, o resultado mais frequente pode não ser uma solução.
- Os valores do array e o target são comparados como **strings**.

---

## Licença

Distribuído sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.
