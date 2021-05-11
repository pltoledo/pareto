import numpy as np
from src.utils import decode

def two_point_crossover(dad, mom, bounds, nbits):
    offspring1 = []
    offspring2 = []
    for varidx in range(len(bounds)):
        first_cpoint = np.random.randint(0, nbits, size=1)[0]
        if first_cpoint == nbits - 1:
            second_cpoint = first_cpoint
            first_cpoint = np.random.randint(0, second_cpoint, size=1)[0]
        else:
            second_cpoint = np.random.randint(first_cpoint + 1, nbits, size=1)[0]

        var_os1 = dad[varidx][:first_cpoint] + mom[varidx][first_cpoint:second_cpoint] + dad[varidx][second_cpoint:]
        var_os2 = mom[varidx][:first_cpoint] + dad[varidx][first_cpoint:second_cpoint] + mom[varidx][second_cpoint:]

        ## Ajusta as variáveis que passarem dos limites estabelecidos
        min, max = bounds[varidx]
        decoded_os1 = decode(var_os1, bounds[varidx])
        if decoded_os1 > max:
            var_os1 = '1111111111'
        elif decoded_os1 < min:
            var_os1 = '0000000000'

        decoded_os2 = decode(var_os2, bounds[varidx])
        if decoded_os2 > max:
            var_os2 = '1111111111'
        elif decoded_os2 < min:
            var_os2 = '0000000000'

        offspring1.append(var_os1)
        offspring2.append(var_os2)
    # O valor da fitness function ainda não é calculado
    offspring1.append(0)
    offspring2.append(0)
    return (offspring1, offspring2)

def sbx_crossover(dad, mom, bounds, eta):
    u = np.random.uniform(size=1)
    if u < 0.5:
        beta = (2*u)**(1 / (eta + 1))
    else:
        beta = (1 / (2*(1 - u)))**(1 / (eta + 1))
    offspring1 = []
    offspring2 = []
    for varidx in range(len(bounds)):
        var_os1 = 0.5*(1 + beta)*dad[varidx] + (1 - beta)*mom[varidx]
        var_os2 = 0.5*(1 - beta)*dad[varidx] + (1 + beta)*mom[varidx]
        # Ajusta as variáveis que passarem dos limites estabelecidos
        min, max = bounds[varidx]
        var_os1 = max if var_os1 > max else min if var_os1 < min else var_os1
        var_os2 = max if var_os2 > max else min if var_os2 < min else var_os2
        # Atribui os valores aos descendentes
        offspring1.append(var_os1)
        offspring2.append(var_os2)

    # O valor da fitness function ainda não é calculado
    offspring1.append(0)
    offspring2.append(0)
    return (offspring1, offspring2)