import numpy as np
from src.utils import decode

def binary_mutation(pop, func, prob, bounds):
    for ind in range(pop.shape[0]):
        for var in range(pop.shape[1]):
            if var == 2:
                pop[ind, var] = func(decode(pop[ind, 0], bounds[0]), decode(pop[ind, 1], bounds[1]))
            else:
                for gene in range(len(pop[ind, var])):
                    u = np.random.uniform(size = 1)
                    if u < prob:
                        pop[ind, var] = pop[ind, var][:gene] + str(1 - int(pop[ind, var][gene])) + pop[ind, var][(gene + 1):]
                    else:
                        continue
    return pop

def real_mutation(pop, func, prob, bounds):
    for ind in range(pop.shape[0]):
        for var in range(pop.shape[1]):
            if var == 2:
                pop[ind, var] = func(pop[ind, 0], pop[ind, 1])
            else:
                u = np.random.uniform(size=1)
                if u < prob:
                    pop[ind, var] = np.random.uniform(low=bounds[var][0], high=bounds[var][1])
                else:
                    continue
    return pop