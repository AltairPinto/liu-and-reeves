from typing import List, Sequence
from numpy import array, zeros


# Eq. 1
def completion_time(m, n, p, pi, i, j):
    # XXX(staticagent): As primeiras linha e coluna são inutilizadas, e estão
    # preenchidas com 0 para servir como dummies na comparação feita por max.
    # Existe um modo de utilizar esse conhecimento para diminuir ainda mais o
    # consumo de memória, mas, no momento, eu tenho que otimizar outras funções.
    c = zeros((i+2, j+2))

    for machine in range(1, c.shape[0]):
        for job in range(1, c.shape[1]):
            lhs = c[machine - 1][job]
            rhs = c[machine][job - 1]

            p_ij = p[machine - 1][pi[job-1]]

            c[machine][job] = max(lhs, rhs) + p_ij

    return c[-1][-1]

# Eq. 2
def total_completion_time(m, n, p, pi):
    # XXX(staticagent): O mesmo comentário em completion_time aplica-se aqui.
    c = zeros((m+1, n+1))

    for machine in range(1, c.shape[0]):
        for job in range(1, c.shape[1]):
            lhs = c[machine - 1][job]
            rhs = c[machine][job - 1]

            p_ij = p[machine - 1][pi[job-1]]

            c[machine][job] = max(lhs, rhs) + p_ij

    return c[-1][-1]

# Eq. 4
def weight(m, n, i, k):
    return m / (i + k*(m - i - 1)/(float)(n - 2)+1)


# Eqs. 6 and 7
def completion_time_if_next(m, n, p, pi, i, j):
    # completion_time
    c = zeros((i+2, len(pi)+1))

    for machine in range(1, c.shape[0]):
        for job in range(1, c.shape[1]):
            lhs = c[machine - 1][job]
            rhs = c[machine][job - 1]

            p_ij = p[machine - 1][pi[job-1]]

            c[machine][job] = max(lhs, rhs) + p_ij

    # completion_time_if_next
    c_next = zeros((i+2))
    for machine in range(1, c_next.shape[0]):
        rhs = c_next[machine - 1]
        lhs = c[machine][-1]

        p_ij = p[machine - 1][j]

        c_next[machine] = max(lhs, rhs) + p_ij

    return c_next[-1]


# Eq. 3
def weighted_total_machine_idle_time(m, n, p, pi, j):
    # completion_time
    c = zeros((m+1, len(pi)+1))

    for machine in range(1, c.shape[0]):
        for job in range(1, c.shape[1]):
            lhs = c[machine - 1][job]
            rhs = c[machine][job - 1]

            p_ij = p[machine - 1][pi[job-1]]

            c[machine][job] = max(lhs, rhs) + p_ij

    # completion_time_if_next
    c_next = zeros((c.shape[0]))
    for machine in range(1, c_next.shape[0]):
        rhs = c_next[machine - 1]
        lhs = c[machine][-1]

        p_ij = p[machine - 1][j]

        c_next[machine] = max(lhs, rhs) + p_ij

    it = 0.

    for i in range(1, m):
        idle_time = max(c_next[i] - c[i+1][-1], 0)
        it += weight(m, n, i, len(pi)) * idle_time

    return it


# Eq. 5
def artificial_processing_time(m, n, p, u, i, j):
    p_a = 0.
    for q in u:
        p_a += p[i][q]

    p_a -= p[i][j]

    return p_a / (len(u) - 1)

# Eqs. 8 and 9
def artificial_completion_time(m, n, p, pi, u, i, j):
    # completion_time
    c = zeros((m+1, len(pi)+1))

    for machine in range(1, c.shape[0]):
        for job in range(1, c.shape[1]):
            lhs = c[machine - 1][job]
            rhs = c[machine][job - 1]

            p_ij = p[machine - 1][pi[job-1]]

            c[machine][job] = max(lhs, rhs) + p_ij

    # completion_time_if_next
    c_next = zeros((c.shape[0]))
    for machine in range(1, c_next.shape[0]):
        lhs = c_next[machine - 1]
        rhs = c[machine][-1]

        p_ij = p[machine - 1][j]

        c_next[machine] = max(lhs, rhs) + p_ij

    # artificial_completion_time
    c_a = zeros((c.shape[0]))
    for machine in range(1, c_a.shape[0]):
        lhs = c_a[machine - 1]
        rhs = c_next[machine]
        p_ia = artificial_processing_time(m, n, p, u, machine-1, j)

        c_a[machine] = max(lhs, rhs) + p_ia

    return c_a[-1]


# Eq. 10
def artificial_total_completion_time(m, n, p, pi, u, j):
    # completion_time
    c = zeros((m+1, len(pi)+1))

    for machine in range(1, c.shape[0]):
        for job in range(1, c.shape[1]):
            lhs = c[machine - 1][job]
            rhs = c[machine][job - 1]

            p_ij = p[machine - 1][pi[job-1]]

            c[machine][job] = max(lhs, rhs) + p_ij

    # completion_time_if_next
    c_next = zeros((c.shape[0]))
    for machine in range(1, c_next.shape[0]):
        lhs = c_next[machine - 1]
        rhs = c[machine][-1]

        p_ij = p[machine - 1][j]

        c_next[machine] = max(lhs, rhs) + p_ij

    # artificial_completion_time
    c_a = zeros((c.shape[0]))
    for machine in range(1, c_a.shape[0]):
        lhs = c_a[machine - 1]
        rhs = c_next[machine]
        p_ia = artificial_processing_time(m, n, p, u, machine-1, j)

        c_a[machine] = max(lhs, rhs) + p_ia

    return c_next[-1] + c_a[-1]


# Eq. 11
def index(m, n, p, pi, u, j):
    it = weighted_total_machine_idle_time(m, n, p, pi, j)
    at = artificial_total_completion_time(m, n, p, pi, u, j)
    return (len(u) - 2)*it + at


def lr(m, n, p, x):
    ranked = sorted(range(0, n), key=lambda j: index(m, n, p, [], range(0, n), j))

    S = []

    for _ in range(0, x):
        pi = list(range(0, n))

        best = ranked.pop(0)
        pi[0], pi[best] = pi[best], pi[0]

        for j in range(1, n-1):
            pi_s, pi_u = pi[:j], pi[j:n]
            u_xi = [index(m, n, p, pi_s, pi_u, u_j) for u_j in pi_u]
            best = min(range(len(pi_u)), key=u_xi.__getitem__)

            pi[j], pi[j + best] = pi[j + best], pi[j]

        S.append(pi)

    # 4. Retornar a sequência com o menor C_sum
    S_C_sum = [total_completion_time(m, n, p, seq) for seq in S]
    best = min(range(len(S_C_sum)), key=S_C_sum.__getitem__)
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
print(lr(m, n, p, 1))
print([2, 16, 8, 14, 13, 15, 5, 18, 12, 6, 11, 10, 7, 1, 0, 19, 3, 9, 4, 17])
