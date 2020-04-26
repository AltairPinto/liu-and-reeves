import numpy as np
from copy import copy

def _l_block_insertion(l, x):
    x = list(x)
    for i in range(len(x)+1-l):
        for j in range(i):  # backward
            yield x[:j] + x[i:i+l] + x[j:i] + x[i+l:]

        for j in range(i+l+1, len(x)+1):  # forward
            yield x[:i] + x[i+l:j] + x[i:i+l] + x[j:]

def _block_swap(l1, l2, x):
    x = list(x)

    for i in range(len(x)+1-l1):
        for j in range(i-l2):  # backward
            print(x[:j], x[i:i+l1], x[j+l2:i], x[j:j+l2], x[i+l1:])

        for j in range(i+l1, len(x)+1-l2):  # forward
            print(x[:i], x[j:j+l2], x[i+l1:j], x[i:i+l1], x[j+l2:])

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
