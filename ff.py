from numpy import array, empty, empty_like


# Eq. 2: Tempo total de conclusão
def total_completion_time(m, n, p, pi):
    c = empty((m, n), dtype=int)

    c[0][0] = p[0][pi[0]]

    for i in range(1, c.shape[0]):
        c[i][0] = c[i-1][0] + p[i][pi[0]]

    for j in range(1, c.shape[1]):
        c[0][j] = c[0][j-1] + p[0][pi[j]]

    for i in range(1, c.shape[0]):
        for j in range(1, c.shape[1]):
            c[i][j] = max(c[i][j-1], c[i-1][j]) + p[i][pi[j]]

    return c[-1][-1]


# Eq. 4: Peso
def weight(m, n, i, k, b):
    return m / (i - b + k*(m - i + b - 1)/(float)(n - 2)+1)


def ff(m, n, p, x, a=4., b=1.):
    # Passo 1: Rankear as tarefas
    xi = empty((n))
    c_k = empty((m))

    for j in range(0, n):
        c_k[0] = p[0][j]
        for i in range(1, c_k.shape[0]):
            c_k[i] = c_k[i-1] + p[i][j]

        xi[j] = c_k[-1]

    ranked = sorted(range(0, n), key=xi.__getitem__)

    # Passo 2: Gerar escalonamentos
    pis = []

    for pi_id in range(0, x):
        pi = list(range(0, n))

        pi_0 = ranked[pi_id]
        pi[0], pi[pi_0] = pi[pi_0], pi[0]

        c = empty((m, n), dtype=int)
        c[0][0] = p[0][pi[0]]
        for i in range(1, c.shape[0]):
            c[i][0] = c[i-1][0] + p[i][pi[0]]

        for k in range(1, n-1):
            pi_u = pi[k:n]

            xi = empty((n-k))
            for j in range(xi.shape[0]):
                c_k = empty((m), dtype=int)
                c_k[0] = c[0][k-1] + p[0][pi_u[j]]
                for i in range(1, c_k.shape[0]):
                    c_k[i] = max(c[i][k-1], c_k[i-1]) + p[i][pi_u[j]]

                it = 0.
                for i in range(1, m):
                    idle_time = max(c_k[i-1] - c[i][k-1], 0)
                    it += weight(m, n, i, k, b) * idle_time

                at = c_k[-1]

                xi[j] = ((n-k-2) / a)*it + at

            pi_s_k = k + min(range(n-k), key=xi.__getitem__)
            pi[k], pi[pi_s_k] = pi[pi_s_k], pi[k]

            c[0][k] = c[0][k-1] + p[0][pi[k]]
            for i in range(1, c.shape[0]):
                c[i][k] = max(c[i][k-1], c[i-1][k]) + p[i][pi[k]]

        pis.append(pi)

    # Passo 3: Retornar escalonamento com menor tempo total de conclusão
    c_sum = [total_completion_time(m, n, p, pi) for pi in pis]
    best = min(range(x), key=c_sum.__getitem__)
    return pis[best]


# dados para teste - ta001
m = 5
n = 20
p = array([
        [54, 83, 15, 71, 77, 36, 53, 38, 27, 87, 76, 91, 14, 29, 12, 77, 32, 87, 68, 94],
        [79,  3, 11, 99, 56, 70, 99, 60,  5, 56,  3, 61, 73, 75, 47, 14, 21, 86,  5, 77],
        [16, 89, 49, 15, 89, 45, 60, 23, 57, 64,  7,  1, 63, 41, 63, 47, 26, 75, 77, 40],
        [66, 58, 31, 68, 78, 91, 13, 59, 49, 85, 85,  9, 39, 41, 56, 40, 54, 77, 51, 31],
        [58, 56, 20, 85, 53, 35, 53, 41, 69, 13, 86, 72,  8, 49, 47, 87, 58, 18, 68, 28]])

pi = ff(m, n, p, 1)
print(pi)
print(total_completion_time(m, n, p, pi))
