from typing import List, Sequence


# Eq. 1
def completion_time(
        m: int,
        n: int,
        p: Sequence[int],
        pi: Sequence[int],
        i: int,
        j: int) -> int:
    assert i < m
    assert j < len(pi)
    assert len(pi) <= n
    assert len(p) == m*n

    # XXX(staticagent): As primeiras linha e coluna são inutilizadas, e estão
    # preenchidas com 0 para servir como dummies na comparação feita por max.
    # Existe um modo de utilizar esse conhecimento para diminuir ainda mais o
    # consumo de memória, mas, no momento, eu tenho que otimizar outras funções.
    c = [0] * ((i+2) * (j+2))

    for machine in range(1, i+2):
        for job in range(1, j+2):
            lhs = c[(machine - 1)*(j+2) + job]
            rhs = c[machine*(j+2) + job - 1]

            p_ij = p[(machine-1)*n + pi[job-1]]

            c[machine*(j+2) + job] = max(lhs, rhs) + p_ij

    return c[-1]

# Eq. 2
def total_completion_time(
        m: int,
        n: int,
        p: Sequence[int],
        pi: Sequence[int]) -> int:
    assert len(p) == m*n
    assert len(pi) == n

    # XXX(staticagent): O mesmo comentário em completion_time aplica-se aqui.
    c = [0] * ((m+1) * (n+1))

    for machine in range(1, m+1):
        for job in range(1, n+1):
            lhs = c[(machine - 1)*(n+1) + job]
            rhs = c[machine*(n+1) + job - 1]
            p_ij = p[(machine-1)*n + pi[job-1]]

            c[machine*(n+1) + job] = max(lhs, rhs) + p_ij

    return c[-1]

# Eq. 4
def weight(
        m: int,
        n: int,
        i: int,
        k: int) -> float:
    assert m >= 0
    assert n > 2
    assert i < m
    assert k < n

    return m / (i + k*(m - i - 1)/(float)(n - 2)+1)


# Eqs. 6 and 7
def completion_time_if_next(
        m: int,
        n: int,
        p: Sequence[int],
        pi: Sequence[int],
        i: int,
        j: int) -> int:
    assert len(p) == m*n
    assert len(pi) < n
    assert i < m
    assert j < n

    if i < 0:
        return 0

    # completion_time
    c = [0] * ((i+2) * (len(pi)+1))

    k = len(pi)-1
    for machine in range(1, i+2):
        for job in range(1, k+2):
            lhs = c[(machine - 1)*(k+2) + job]
            rhs = c[machine*(k+2) + job - 1]

            p_ij = p[(machine-1)*n + pi[job-1]]

            c[machine*(k+2) + job] = max(lhs, rhs) + p_ij

    # completion_time_if_next
    c_next = [0] * (i+2)
    for machine in range(1, i+2):
        rhs = c_next[machine - 1]
        lhs = c[(machine)*(k+2) + k+1]

        p_ij = p[(machine-1)*n + j]

        c_next[machine] = max(lhs, rhs) + p_ij

    return c_next[-1]


# Eq. 3
def weighted_total_machine_idle_time(
        m: int,
        n: int,
        p: Sequence[int],
        pi: Sequence[int],
        j: int) -> float:
    assert len(p) == m*n
    assert len(pi) < n
    assert j < n

    it = 0.

    for i in range(1, m):
        idle_time = max(completion_time_if_next(m, n, p, pi, i-1, j) - completion_time(m, n, p, pi, i, len(pi)-1), 0)
        it += weight(m, n, i, len(pi)) * idle_time

    return it


# Eq. 5
def artificial_processing_time(
        m: int,
        n: int,
        p: Sequence[int],
        u: Sequence[int],
        i: int,
        j: int) -> float:
    assert len(p) == m*n
    assert len(u) <= n
    assert len(u) > 1
    assert i < m
    assert j < n

    p_a = 0.
    for q in u:
        p_a += p[i*n + q]

    p_a -= p[i*n + j]

    return p_a / (len(u) - 1)

# Eqs. 8 and 9
def artificial_completion_time(
        m: int,
        n: int,
        p: Sequence[int],
        pi: Sequence[int],
        u: Sequence[int],
        i: int,
        j: int) -> float:
    assert len(p) == m*n
    assert len(pi)+len(u) == n
    assert len(u) > 1
    assert i < m
    assert j < n

    if i < 0:
        return 0.

    lhs = float(completion_time_if_next(m, n, p, pi, i, j))
    rhs = artificial_completion_time(m, n, p, pi, u, i-1, j)
    p_ia = artificial_processing_time(m, n, p, u, i, j)
    return max(lhs, rhs) + p_ia


# Eq. 10
def artificial_total_completion_time(
        m: int,
        n: int,
        p: Sequence[int],
        pi: Sequence[int],
        u: Sequence[int],
        j: int) -> float:
    assert len(p) == m*n
    assert len(pi)+len(u) == n
    assert len(u) > 1
    assert j < n

    c_j = completion_time_if_next(m, n, p, pi, m-1, j)
    c_a = artificial_completion_time(m, n, p, pi, u, m-1, j)
    return c_j + c_a


# Eq. 11
def index(
        m: int,
        n: int,
        p: Sequence[int],
        pi: Sequence[int],
        u: Sequence[int],
        j: int) -> float:
    it = weighted_total_machine_idle_time(m, n, p, pi, j)
    at = artificial_total_completion_time(m, n, p, pi, u, j)
    return (len(u) - 2)*it + at


def lr(
        m: int,
        n: int,
        p: Sequence[int],
        x: int) -> List[int]:
    assert m > 0
    assert n > 2
    assert len(p) == m*n
    assert x >= 1
    assert x <= n

    pi_base = list(range(0, n))
    ranked = sorted(pi_base, key=lambda j: index(m, n, p, pi_base[:0], pi_base[0:n], j))

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
p = [
        54, 83, 15, 71, 77, 36, 53, 38, 27, 87, 76, 91, 14, 29, 12, 77, 32, 87, 68, 94,
        79,  3, 11, 99, 56, 70, 99, 60,  5, 56,  3, 61, 73, 75, 47, 14, 21, 86,  5, 77,
        16, 89, 49, 15, 89, 45, 60, 23, 57, 64,  7,  1, 63, 41, 63, 47, 26, 75, 77, 40,
        66, 58, 31, 68, 78, 91, 13, 59, 49, 85, 85,  9, 39, 41, 56, 40, 54, 77, 51, 31,
        58, 56, 20, 85, 53, 35, 53, 41, 69, 13, 86, 72,  8, 49, 47, 87, 58, 18, 68, 28]
print(lr(m, n, p, 1) == [2, 16, 8, 14, 13, 15, 5, 18, 12, 6, 11, 10, 7, 1, 0, 19, 3, 9, 4, 17])
