from copy import copy
from random import randint
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

def insert(pi, i, j):
    tmp = copy(pi)
    elem = tmp.pop(i)
    tmp.insert(j, elem)
    return tmp

# Algorithm 1
def job_insert(m, n, p, pi, i):
    c_sum = total_completion_time(m, n, p, pi)

    for j in range(0, n):
        if i == j:
            continue
        candidate = insert(pi, i, j)
        if total_completion_time(m, n, p, candidate) < c_sum:
            return candidate

    return pi

# Algorithm 2
def interchange(m, n, p, pi, i):
    c_sum = total_completion_time(m, n, p, pi)
    candidate = copy(pi)

    for j in range(i+1, n):
        # troca
        candidate[i], candidate[j] = candidate[j], candidate[i]

        if total_completion_time(m, n, p, candidate) < c_sum:
            return candidate

        # destroca
        candidate[i], candidate[j] = candidate[j], candidate[i]

    return pi

# Algorithm 3
def reduced_ji(m, n, p, pi):
    improve = False
    new_pi = copy(pi)
    c_sum = total_completion_time(m, n, p, pi)

    for i in range(0, n):
        candidate = job_insert(m, n, p, pi, i)
        new_c_sum = total_completion_time(m, n, p, candidate)
        if new_c_sum < c_sum:
            improve = True
            new_pi = copy(candidate)
            c_sum = new_c_sum

    return improve, new_pi

# Algorithm 4
def reduced_interchange(m, n, p, pi):
    improve = False
    new_pi = copy(pi)
    c_sum = total_completion_time(m, n, p, pi)

    for i in range(0, n):
        candidate = interchange(m, n, p, pi, i)
        new_c_sum = total_completion_time(m, n, p, candidate)
        if new_c_sum < c_sum:
            improve = True
            new_pi = copy(candidate)
            c_sum = new_c_sum

    return improve, new_pi

# Algorithm 5
def job_insert_ls(m, n, p, pi, iter_max):
    new_pi = pi

    # FIXME: mudar iter_max para ser tempo de CPU máximo
    for i in range(0, iter_max):
        condition, new_pi = reduced_ji(m, n, p, new_pi)
        if not condition:
            # Não houve melhora
            break

    return new_pi

# Algorithm 6
def job_interchange_ls(m, n, p, pi, iter_max):
    new_pi = pi

    # FIXME: mudar iter_max para ser tempo de CPU máximo
    for i in range(0, iter_max):
        condition, new_pi = reduced_interchange(m, n, p, new_pi)
        if not condition:
            # Não houve melhora
            break

    return new_pi

def shake(pi):
    pi_shaken = copy(pi)

    # Num de movimentos
    n_moves = randint(3, 5)

    for _ in range(0, n_moves):
        # Tarefas a serem trocadas de lugar
        i = randint(0, len(pi)-1)
        j = randint(0, len(pi)-1)

        pi_shaken[i], pi_shaken[j] = pi_shaken[j], pi_shaken[i]

    return pi_shaken

def vns4(m, n, p, x, iter_max):
    pi = x
    best_solution = pi

    # FIXME: trocar número de iterações por tempo de CPU
    for _ in range(0, iter_max):
        condition = True

        # FIXME: trocar número de iterações por tempo de CPU
        for _ in range(0, iter_max):
            pi = job_interchange_ls(m, n, p, pi, iter_max)
            condition, pi = reduced_ji(m, n, p, pi)

            if not condition:
                # Não houve melhora
                break

        if total_completion_time(m, n, p, pi) < total_completion_time(m, n, p, best_solution):
            best_solution = pi

        pi = best_solution

        pi = shake(pi)
    return best_solution


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

k_max = 5
iter_max = 10

res = vns4(m, n, p, x, k_max, iter_max)
print(res)
print(total_completion_time(m, n, p, res))
