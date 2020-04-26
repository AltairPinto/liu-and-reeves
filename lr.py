from typing import List, Sequence
from numpy import array, zeros


# Eq. 2: Tempo total de conclusão
def total_completion_time(m, n, p, pi):
    # XXX(staticagent): As primeiras linha e coluna são inutilizadas, e estão
    # preenchidas com 0 para servir como dummies na comparação feita por max.
    # Existe um modo de utilizar esse conhecimento para diminuir ainda mais o
    # consumo de memória, mas, no momento, eu tenho que otimizar outras funções.
    c = zeros((m+1, n+1))

    for machine in range(1, c.shape[0]):
        for job in range(1, c.shape[1]):
            lhs = c[machine - 1][job]
            rhs = c[machine][job - 1]

            p_ij = p[machine - 1][pi[job-1]]

            c[machine][job] = max(lhs, rhs) + p_ij

    return c[-1][-1]


# Eq. 4: Peso
def weight(m, n, i, k):
    return m / (i + k*(m - i - 1)/(float)(n - 2)+1)


# Eq. 5: Tempo de processamento da tarefa artificial
def artificial_processing_time(m, n, p, pi, k, i, j):
    p_a = 0.
    for q in pi[k:n]:
        p_a += p[i][q]
    p_a -= p[i][j]

    return p_a / (n-k-1)


# Eq. 11
def index(m, n, p, pi, k, j):
    # Eq. 1: Tempo de conclusão

    # XXX(staticagent): As primeiras linha e coluna são inutilizadas, e estão
    # preenchidas com 0 para servir como dummies na comparação feita por max.
    # Existe um modo de utilizar esse conhecimento para diminuir ainda mais o
    # consumo de memória, mas, no momento, eu tenho que otimizar outras funções.
    c = zeros((m+1, k+1))

    for machine in range(1, c.shape[0]):
        for job in range(1, c.shape[1]):
            lhs = c[machine - 1][job]
            rhs = c[machine][job - 1]

            p_ij = p[machine - 1][pi[job-1]]

            c[machine][job] = max(lhs, rhs) + p_ij

    # Eqs. 6 e 7: Tempo de conclusão da tarefa j se escalonada
    c_next = zeros((c.shape[0]))
    for machine in range(1, c_next.shape[0]):
        rhs = c_next[machine - 1]
        lhs = c[machine][-1]

        p_ij = p[machine - 1][j]

        c_next[machine] = max(lhs, rhs) + p_ij

    # Eq. 3: Tempo total de ociosidade de máquina poderado
    it = 0.
    for i in range(1, m):
        idle_time = max(c_next[i] - c[i+1][-1], 0)
        it += weight(m, n, i, k) * idle_time

    # Eq. 8 e 9: Tempo de conclusão da tarefa artificial
    c_a = zeros((c.shape[0]))
    for machine in range(1, c_a.shape[0]):
        lhs = c_a[machine - 1]
        rhs = c_next[machine]
        p_ia = artificial_processing_time(m, n, p, pi, k, machine-1, j)

        c_a[machine] = max(lhs, rhs) + p_ia

    # Eq. 10: Tempo total de conclusão artificial
    at = c_next[-1] + c_a[-1]

    return (n-k-2)*it + at


def lr(m, n, p, x):
    ranked = sorted(range(0, n), key=lambda j: index(m, n, p, range(0, n), 0, j))

    S = []

    for _ in range(0, x):
        pi = list(range(0, n))

        best = ranked.pop(0)
        pi[0], pi[best] = pi[best], pi[0]

        for k in range(1, n-1):
            xi = [index(m, n, p, pi, k, j) for j in pi[k:n]]
            best = min(range(n-k), key=xi.__getitem__)
            pi[k], pi[k+best] = pi[k+best], pi[k]

        S.append(pi)

    c_sum = [total_completion_time(m, n, p, seq) for seq in S]
    best = min(range(x), key=c_sum.__getitem__)
    return S[best]


# dados para teste - ta001
m = 5
n = 20
p = array([
        [54, 83, 15, 71, 77, 36, 53, 38, 27, 87, 76, 91, 14, 29, 12, 77, 32, 87, 68, 94],
        [79,  3, 11, 99, 56, 70, 99, 60,  5, 56,  3, 61, 73, 75, 47, 14, 21, 86,  5, 77],
        [16, 89, 49, 15, 89, 45, 60, 23, 57, 64,  7,  1, 63, 41, 63, 47, 26, 75, 77, 40],
        [66, 58, 31, 68, 78, 91, 13, 59, 49, 85, 85,  9, 39, 41, 56, 40, 54, 77, 51, 31],
        [58, 56, 20, 85, 53, 35, 53, 41, 69, 13, 86, 72,  8, 49, 47, 87, 58, 18, 68, 28]])

pi = lr(m, n, p, 1)
print(pi)
print(total_completion_time(m, n, p, pi))
