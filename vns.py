from numpy import array, empty

# função objetivo
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


# Algorithm 1
def neighborhood_change(m, n, p, x, x_prime, k):
    if total_completion_time(m, n, p, x_prime) < total_completion_time(m, n, p, x):
        return x_prime, 1
    else:
        return x, k+1


def vns(m, n, p, x, k_max, iter_max):
    # FIXME: trocar iterações por tempo de CPU?
    # FIXME: o número de iterações deve zerar se houver uma melhora
    for t in range(0, iter_max):
        k = 1

        while k < k_max:
            # TODO: shake

            # TODO: local_optimum (via local search)
            x_prime = x

            # Mudança de vizinhança
            x, k = neighborhood_change(m, n, p, x, x_prime, k)

    return x

m = 5
n = 20
p = array([
        [54, 83, 15, 71, 77, 36, 53, 38, 27, 87, 76, 91, 14, 29, 12, 77, 32, 87, 68, 94],
        [79,  3, 11, 99, 56, 70, 99, 60,  5, 56,  3, 61, 73, 75, 47, 14, 21, 86,  5, 77],
        [16, 89, 49, 15, 89, 45, 60, 23, 57, 64,  7,  1, 63, 41, 63, 47, 26, 75, 77, 40],
        [66, 58, 31, 68, 78, 91, 13, 59, 49, 85, 85,  9, 39, 41, 56, 40, 54, 77, 51, 31],
        [58, 56, 20, 85, 53, 35, 53, 41, 69, 13, 86, 72,  8, 49, 47, 87, 58, 18, 68, 28]])

# Resultado dado por LR(1)
x = [2, 16, 8, 14, 13, 15, 5, 18, 12, 6, 11, 10, 7, 1, 0, 19, 3, 9, 4, 17]

k_max = 1
iter_max = 1000

res = vns(m, n, p, x, k_max, iter_max)
print(res)
print(total_completion_time(m, n, p, res))
