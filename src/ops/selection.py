import numpy as np

def tournament_selection(pop, n_candidates, n_champions=2):
    champions = []
    for l in range(n_champions):
        tourn = np.random.choice(range(pop.shape[0]), size=n_candidates, replace=False)
        candidates = pop[tourn, :]
        champions.append(candidates[np.argsort(candidates[:, 2])][0, [0, 1]])
    return champions
