import numpy as np
from copy import copy


def _l_block_insertion(l, x):
    assert l > 1

    x = np.array(x)

    # Each outer iteration creates a block whose length is given by l,

    # Each outer iteration creates a block of size l.  So we iterate from the
    # very beginning to past the end of x, always respecting the requirement of
    # the block being of lenght l.
    
    # We iterate from the very beginning to past the end of x, always respecting the fact that 
    for i in range(len(x)+1-l):
        for j in range(i):  # Backward iteration
            pass

        for j in range(i+l+1
    
    x = list(x)
    for i in range(len(x)+1-l):
        for j in range(i):  # backward
            yield x[:j] + x[i:i+l] + x[j:i] + x[i+l:]

        for j in range(i+l+1, len(x)+1):  # forward
            yield x[:i] + x[i+l:j] + x[i:i+l] + x[j:]



def _block_swap2(l1, l2, x):
    assert l1 >= 1
    assert l2 >= 0

    x = np.array(x)

    # Conceitualmente, a vizinhança Block Swap divide x em 5 blocos; os blocos
    # 1, 3 e 5 ficam imóveis, enquanto os blocos 2 e 4 trocam de lugar.
    #
    #     x  = b1 + b2 + b3 + b4 + b5
    #     nx = b1 + b4 + b3 + b2 + b5
    #
    # Cada iteração de i cria um bloco cujos índice em x e tamanho são dados,
    # respectivamente, por i e l1.  Esse é o bloco b2 como mostrado acima.
    #
    # Podemos gerar len(x)-l1+1 blocos b2 a partir de x.  E.g.: se l1 = 1,
    # podemos gerar len(x)-1+1 = len(x) blocos, enquanto que se l1 = 2, podemos
    # gerar len(x)-2+1 = len(x)-1 blocos.  Note que essa fórmula garante a
    # restrição de que todos os blocos gerados tenham tamanho l1, i.e., novos
    # blocos serão gerados enquanto o número de elementos ainda a serem
    # visitados em x for maior ou igual a l1.
    n_b2 = len(x)+1-l1
    for i in range(n_b2):

        n_b4 = i - l2
        for j in range(n_b4):
            pass



def _block_swap(l1, l2, x):
    x = list(x)

    for i in range(len(x)+1-l1):
        for j in range(i-l2):  # backward
            yield x[:j] + x[i:i+l1] + x[j+l2:i] + x[j:j+l2] + x[i+l1:]

        for j in range(i+l1, len(x)+1-l2):  # forward
            yield x[:i] + x[j:j+l2] + x[i+l1:j] + x[i:i+l1] + x[j+l2:]


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
