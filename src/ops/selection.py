import numpy as np

class Selector:
    
    def __init__(self, method, n_parents=2):
        self.method = method
        self.n_parents = n_parents

    def tournament_selection(self, pop, n_candidates):
        champions = []
        for l in range(self.n_parents):
            tourn = np.random.choice(range(pop.shape[0]), size=n_candidates, replace=False)
            candidates = pop[tourn, :]
            sorted_index = np.argsort(candidates[:, 2])[::-1]
            sorted_pop = candidates[sorted_index, :]
            champions.append(sorted_pop[0, [0, 1]])
        return champions

    def roulette_wheel_selection(self, pop):
        sum_fitness = np.sum(pop[:, 2])
        sort_index = np.argsort(pop[:, 2])
        sorted_pop = pop[sort_index, :]
        prob_array = np.cumsum(sorted_pop[:, 2] / sum_fitness)
        champions = []
        while len(champions) < self.n_parents:
            u = np.random.uniform(size=1)
            for index, p in enumerate(prob_array):
                if p <= u:
                    champions.append(sorted_pop[index, [0, 1]])
                    break
        return champions

    def select(self, pop, n_candidates=None):

        if self.method == 'tournament':
            return self.tournament_selection(pop, n_candidates)
        if self.method == 'roulette':
            return self.roulette_wheel_selection(pop)