import numpy as np
from copy import copy

def _l_block_insertion_forward(l, x):
    x = list(x)
    for i in range(len(x)-l):

        # FIXME: the backward iteration is buggy
        for j in range(0, i+l+1):  # backward
            print(x[i:i+l], x[:i], x[i+l:j], x[j:])

        for j in range(i+l+1, len(x)+1):  #forward
            print(x[:i], x[i+l:j], x[i:i+l], x[j:])

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
