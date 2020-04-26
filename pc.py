from copy import copy
from functools import partial
from random import choice, randint
from time import time

import numpy as np


# p = n * m
p = np.array([
    [54, 79, 16, 66, 58],
    [83,  3, 89, 58, 56],
    [15, 11, 49, 31, 20],
    [71, 99, 15, 68, 85],
    [77, 56, 89, 78, 53],
    [36, 70, 45, 91, 35],
    [53, 99, 60, 13, 53],
    [38, 60, 23, 59, 41],
    [27,  5, 57, 49, 69],
    [87, 56, 64, 85, 13],
    [76,  3,  7, 85, 86],
    [91, 61,  1,  9, 72],
    [14, 73, 63, 39,  8],
    [29, 75, 41, 41, 49],
    [12, 47, 63, 56, 47],
    [77, 14, 47, 40, 87],
    [32, 21, 26, 54, 58],
    [87, 86, 75, 77, 18],
    [68,  5, 77, 51, 68],
    [94, 77, 40, 31, 28]])

# Resultado dado por LR(1)
x_lr = np.array(
    [2, 16, 8, 14, 13, 15, 5, 18, 12, 6, 11, 10, 7, 1, 0, 19, 3, 9, 4, 17])


def _c_sum(p, pi):
    c = p[pi]

    # XXX: é possível vetorizar o loop mais adentro, utilizando a técnica de
    #  polytype model; para mais info, observar as diagonais segundárias de c

    np.cumsum(c[0], out=c[0])
    np.cumsum(c[:,0], out=c[:,0])

    for i in range(1, c.shape[0]):
        for j in range(1, c.shape[1]):
            c[i][j] += max(c[i-1][j], c[i][j-1])

    return np.sum(c[:,-1])

def _ff(p, x, a=4., b=1.):
    n, m = p.shape

    weight = lambda i, k: m / (i - b + k*(m - i + b - 1)/(float)(n - 2)+1)

    assert x > 0
    assert x <= n

    # Passo 1: Ranquear tarefas
    ranked = p.sum(1).argsort()

    # Passo 2: Gerar escalonamentos
    pis = []

    for pi_0 in ranked[:x]:
        pi = np.array(range(n))
        c = np.empty_like(p)

        # Get the first job
        pi[pi_0], pi[0] = pi[0], pi_0

        c[0] = p[pi_0]
        c[0].cumsum(out=c[0])

        for k in range(1, n-1):
            pi_u = pi[k:]

            xi = np.empty_like(pi_u)
            for j in range(pi_u.shape[0]):
                c_k = np.empty((m))
                c_k[0] = c[k-1][0] + p[pi_u[j]][0]
                for i in range(1, m):
                    c_k[i] = max(c[k-1][i], c_k[i-1]) + p[pi_u[j]][i]

                it = 0.
                for i in range(1, m):
                    idle_time = max(c_k[i-1] - c[k-1][i], 0)
                    it += weight(i, k) * idle_time

                at = c_k[-1]

                xi[j] = ((n-k-2) / a)*it + at

            pi_k = k + min(range(n-k), key=xi.__getitem__)
            pi[k], pi[pi_k] = pi[pi_k], pi[k]

            c[k][0] = c[k-1][0] + p[pi[k]][0]
            for i in range(1, m):
                c[k][i] = max(c[k-1][i], c[k][i-1]) + p[pi[k]][i]

        pis.append(pi)

    # Passo 3: Retornar escalonamento com menor tempo total de conclusão
    cost = partial(_c_sum, p)
    c_sum = [cost(pi) for pi in pis]
    best = min(range(x), key=c_sum.__getitem__)
    return pis[best]


def _l_block_insertion(l, x):
    assert l > 0

    x = np.array(x)

    for i in range(len(x)-l+1):
        b3 = x[i:i+l]
        b4 = x[i+l:]
        for j in range(i):  # Backward iteration
            b1 = x[:j]
            b2 = x[j:i]
            yield np.concatenate((b1, b3, b2, b4)).ravel()

        b1 = x[:i]
        b2 = x[i:i+l]
        for j in range(i+l+1, len(x)+1):  # Forward iteration
            b3 = x[i+l:j]
            b4 = x[j:]
            yield np.concatenate((b1, b3, b2, b4)).ravel()


def _block_swap(l, l_swap, x):
    assert l > 0

    x = np.array(x)

    for i in range(len(x)-l+1):
        b4 = x[i:i+l]
        b5 = x[i+l:]
        for j in range(i-l_swap+1):  # Backward iteration
            b1 = x[:j]
            b2 = x[j:j+l_swap]
            b3 = x[j+l_swap:i]
            yield np.concatenate((b1, b4, b3, b2, b5)).ravel()

        b1 = x[:i]
        b2 = x[i:i+l]
        for j in range(i+l, len(x)-l_swap+1):  # Forward iteration
            b3 = x[i+l:j]
            b4 = x[j:j+l_swap]
            b5 = x[j+l_swap:]
            yield np.concatenate((b1, b4, b3, b2, b5)).ravel()


def rvnd(cost, L_, x):
    # Inicialize a lista de vizinhanças L
    L = copy(L_)

    # Enquanto L tiver elementos:
    while len(L) > 0:

        # Selecione uma vizinhança N dentro de L de forma aleatória
        N = choice(L)

        # Encontre o melhor vizinho pi' de pi dentro de N
        best = None
        best_cost = float('inf')
        for x_n in N(x):
            x_n_cost = cost(x_n)
            if x_n_cost < best_cost:
                best, best_cost = x_n, x_n_cost

        # se total_completion_time(pi') < total_completion_time(pi):
        if best_cost < cost(x):
            # pi = pi'
            x = best

            # atualize L
            L = copy(L_)
        else:
            # remova N de L
            L.remove(N)

    return x



def _multiple_swap(l1, l2, x):
    if randint(0, 1) == 0:
        l1, l2 = l2, l1

    newx = x
    for _ in range(randint(1, 3)):
        i = randint(0, len(x)-l1-l2)
        j = randint(i+l1, len(x)-l2)

        b1 = newx[:i]
        b2 = newx[i:i+l1]
        b3 = newx[i+l1:j]
        b4 = newx[j:j+l2]
        b5 = newx[j+l2:]
        newx = np.concatenate((b1, b4, b3, b2, b5)).ravel()

    return newx

def shake(l1, l2, x):
    if randint(0, 1) == 0:
        newx = _multiple_swap(l1, l2, x)
        if not np.array_equal(newx, x):
            return newx

    newx = _multiple_swap(1, 1, x)
    return newx


# cputime é dado em segundos: cputime=30. -> 30 segundos
def ils(p, cputime):
    # função de custo
    cost = lambda x: _c_sum(p, x)

    # vizinhanças
    L = [
        lambda x: _l_block_insertion(1, x),
        lambda x: _l_block_insertion(2, x),  # XXX: modificar valor ao seu bel prazer
        lambda x: _block_swap(1, 1, x),
        lambda x: _block_swap(1, 2, x),
        lambda x: _block_swap(1, 3, x),
        lambda x: _block_swap(2, 2, x),
        lambda x: _block_swap(2, 3, x),  # XXX: modificar valores ao seu bel prazer
        lambda x: _block_swap(2, 4, x),
        lambda x: _block_swap(3, 3, x),
        lambda x: _block_swap(3, 4, x),
        lambda x: _block_swap(4, 4, x)
    ]

    n, m = p.shape

    start = time()

    s_0 = _ff(p, round(n/m))  # XXX: FF(x) tem alguns parâmetros, pode mexer neles
    s_new = rvnd(cost, L, s_0)
    s_new_cost = cost(s_new)

    while time() - start < cputime:
        s_shaken = shake(2, 3, s_new)  # XXX: modificar valores ao seu bel prazer
        s_tmp = rvnd(cost, L, s_shaken)
        s_tmp_cost = cost(s_tmp)

        # Critério de aceitação
        if s_tmp_cost < s_new_cost:
            s_new, s_new_cost = s_tmp, s_tmp_cost

    return s_new


def vns(p, cputime):
    # função de custo
    cost = lambda x: _c_sum(p, x)

    # vizinhanças
    L = [
        lambda x: _l_block_insertion(2, x),  # XXX: modificar valor ao seu bel prazer
        lambda x: _block_swap(2, 3, x)  # XXX: modiicar valores ao seu bel prazer
    ]
    L_ = copy(L)

    n, m = p.shape

    start = time()

    s_0 = _ff(p, round(n/m)) # XXX: FF(x) tem alguns parâmetros, pode mexer neles
    s_new = s_0
    s_new_cost = cost(s_new)

    while time() - start < cputime:
        k = 0
        while k < len(L):
            N = L[k]
            s_tmp = choice(list(N(s_new)))
            s_tmp2 = rvnd(cost, L, s_tmp)
            s_tmp2_cost = cost(s_tmp2)

            # Critério de aceitação
            if s_tmp2_cost < s_new_cost:
                s_new, s_new_cost = s_tmp2, s_tmp2_cost

                # reseta lista de vizinhanças
                k = 1
            else:
                # passa p/ próxima vizinhança
                k += 1

    return s_new
