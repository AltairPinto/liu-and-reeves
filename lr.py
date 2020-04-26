from numpy import array, zeros


# Eq. 2: Tempo total de conclusão
def total_completion_time(m, n, p, pi):
    # XXX(staticagent): As primeiras linha e coluna são inutilizadas, e estão
    # preenchidas com 0 para servir como dummies na comparação feita por max.
    # Existe um modo de utilizar esse conhecimento para diminuir ainda mais o
    # consumo de memória, mas, no momento, eu tenho que otimizar outras funções.
    c = zeros((m+1, n+1), dtype=int)

    for i in range(1, c.shape[0]):
        for j in range(1, c.shape[1]):
            left = c[i-1][j]
            up = c[i][j-1]
            proc_time = p[i-1][pi[j-1]]
            c[i][j] = max(left, up) + proc_time

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
def index(m, n, p, pi, k, pi_j):
    # Eq. 1: Tempo de conclusão

    # XXX(staticagent): As primeiras linha e coluna são inutilizadas, e estão
    # preenchidas com 0 para servir como dummies na comparação feita por max.
    # Existe um modo de utilizar esse conhecimento para diminuir ainda mais o
    # consumo de memória, mas, no momento, eu tenho que otimizar outras funções.
    c = zeros((m+1, k+1), dtype=int)
    for i in range(1, c.shape[0]):
        for j in range(1, c.shape[1]):
            left = c[i-1][j]
            up = c[i][j-1]
            proc_time = p[i-1][pi[j-1]]
            c[i][j] = max(left, up) + proc_time

    # Eqs. 6 e 7: Tempo de conclusão da tarefa j se escalonada
    c_k = zeros((m+1), dtype=int)
    for i in range(1, c_k.shape[0]):
        left = c_k[i-1]
        up = c[i][-1]
        proc_time = p[i-1][pi_j]
        c_k[i] = max(left, up) + proc_time

    # Eq. 8 e 9: Tempo de conclusão da tarefa artificial
    c_kp1 = zeros((m+1))
    for i in range(1, c_kp1.shape[0]):
        left = c_kp1[i-1]
        up = c_k[i]
        proc_time = artificial_processing_time(m, n, p, pi, k, i-1, pi_j)
        c_kp1[i] = max(left, up) + proc_time

    # Eq. 3: Tempo total de ociosidade de máquina poderado
    it = 0.
    for i in range(1, m):
        idle_time = max(c_k[i] - c[i+1][-1], 0)
        it += weight(m, n, i, k) * idle_time

    # Eq. 10: Tempo total de conclusão artificial
    at = c_k[-1] + c_kp1[-1]

    return (n-k-2)*it + at


def lr(m, n, p, x):
    ranked = sorted(range(0, n), key=lambda j: index(m, n, p, range(0, n), 0, j))

    pis = []

    for pi_id in range(0, x):
        pi = list(range(0, n))

        pi_0 = ranked[pi_id]
        pi[0], pi[pi_0] = pi[pi_0], pi[0]

        for k in range(1, n-1):
            xi = [index(m, n, p, pi, k, j) for j in pi[k:n]]
            pi_k = k + min(range(n-k), key=xi.__getitem__)
            pi[k], pi[pi_k] = pi[pi_k], pi[k]

        pis.append(pi)

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

pi = lr(m, n, p, 1)
print(pi)
print(total_completion_time(m, n, p, pi))
