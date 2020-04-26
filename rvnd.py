import numpy as np


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
        for j in range(i+l, len(x)+1):  # Forward iteration
            b3 = x[i+l:j]
            b4 = x[j:]
            yield np.concatenate((b1, b3, b2, b4)).ravel()


def _block_swap(l, l_swap, x):
    assert l      > 0
    assert l_swap > 0

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


def rvnd(p, x):
    pi = x

    # Inicialize a lista de vizinhanças L

    # Enquanto L tiver elementos:
    #   Selecione uma vizinhança N dentro de L de forma aleatória
    #   Encontre o melhor vizinho pi' de pi dentro de N
    #   se total_completion_time(pi') < total_completion_time(pi):
    #     pi = pi'
    #     atualize L
    #   senão
    #     remova N de L

    return pi
