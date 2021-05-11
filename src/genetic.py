import streamlit as st
import numpy as np
from src.utils import decode



class BinaryEvolver:

    def __init__(self):
        pass
    
    def generate_pop(self, npop, nbits=10, bounds=[(-5, 5), (-5,  5)]):
        
        pop = np.empty((npop, 3), dtype = 'object')
        xmin, xmax = bounds[0]
        ymin, ymax = bounds[1]

        for i in range(npop):
            pop[i, 0] = ''.join([str(j) for j in np.random.randint(0, 2, nbits)])
            pop[i, 1] = ''.join([str(j) for j in np.random.randint(0, 2, nbits)])

        self.initial_pop = pop
        self.npop = npop
        self.nbits = nbits
        self.bounds = bounds

    def evolve(self, f, maxgen, pc=0.9, n_tourn=2):
        
        xmin, xmax = self.bounds[0]
        ymin, ymax = self.bounds[1]
        pop = self.initial_pop

        for i in range(self.npop):
            pop[i, 2] = f(decode(pop[i, 0], xmin, xmax), decode(pop[i, 1], ymin, ymax))

        pm = 1 / (self.npop * np.sqrt(self.nbits)) # Probabilida de mutação

        # Inicializa a população selecionando valores aleatórios
        ngen = 0
        while ngen < maxgen:
            next_gen = np.empty((1, 3), dtype='object')[1::]

            # Preenche a próxima geração
            while next_gen.shape[0] < self.npop:

                # Utiliza torunament selection para criar o mating pool
                champions = []
                for l in range(2):
                    tourn = np.random.choice(range(self.npop), size = n_tourn, replace = False)
                    candidates = pop[tourn, :]
                    champions.append(candidates[np.argsort(candidates[:, 2])][0, [0, 1]])
                dad, mom = champions

                # Faz o crossover utilizando 2 point crossover
                if np.random.uniform(size=1) < pc:
                    offspring1 = []
                    offspring2 = []
                    for i in range(len(self.bounds)):
                        first_cpoint = np.random.randint(0, self.nbits, size=1)[0]
                        if first_cpoint == self.nbits - 1:
                            second_cpoint = first_cpoint
                            first_cpoint = np.random.randint(0, second_cpoint, size=1)[0]
                        else:
                            second_cpoint = np.random.randint(first_cpoint + 1, self.nbits, size=1)[0]

                        var1 = dad[i][:first_cpoint] + mom[i][first_cpoint:second_cpoint] + dad[i][second_cpoint:]
                        var2 = mom[i][:first_cpoint] + dad[i][first_cpoint:second_cpoint] + mom[i][second_cpoint:]

                        ## Ajusta as variáveis que passarem dos limites estabelecidos

                        if decode(var1, self.bounds[i][0], self.bounds[i][1]) > self.bounds[i][1]:
                            var1 = '1111111111'
                        elif decode(var1, self.bounds[i][0], self.bounds[i][1]) < self.bounds[i][0]:
                            var1 = '0000000000'
                        
                        if decode(var2, self.bounds[i][0], self.bounds[i][1]) > self.bounds[i][1]:
                            var2 = '1111111111'
                        elif decode(var2, self.bounds[i][0], self.bounds[i][1]) < self.bounds[i][0]:
                            var2 = '0000000000'

                        offspring1.append(var1)
                        offspring2.append(var2)

                    # o valor da fitness function ainda não é calculado
                    offspring1.append(0)
                    offspring2.append(0)

                    # Acrescenta o indivíduo a próxima geração
                    next_gen = np.vstack((next_gen, np.array(offspring1), np.array(offspring2)))
            
            # Realiza a mutação nos indivíduos da geração seguinte
            for i in range(next_gen.shape[0]):
                for j in range(next_gen.shape[1]):
                    if j == 2:
                        next_gen[i, j] = f(decode(next_gen[i, 0], xmin, xmax), decode(next_gen[i, 1], ymin, ymax))
                    else:
                        for k in range(len(next_gen[i, j])):
                            u = np.random.uniform(size = 1)
                            if u < pm:
                                next_gen[i, j] = next_gen[i, j][:k] + str(1 - int(next_gen[i, j][k])) + next_gen[i, j][(k + 1):]
                            else:
                                continue
            
            # Junta as duas populações e seleciona os npop-melhores indivíduos
            joined_pop = np.vstack((pop, next_gen))
            pop = joined_pop[np.argsort(joined_pop[:, 2])][range(self.npop), :]
            ngen += 1
        
        # Retorna a população com os valores decodificados
        for i in range(self.npop):
            pop[i, 0] = decode(pop[i, 0], xmin, xmax)
            pop[i, 1] =  decode(pop[i, 1], ymin, ymax)
        self.final_gen = pop

class RealEvolver:

    def __init__(self):
        pass
    
    def generate_pop(self, npop, bounds=[(-5, 5), (-5,  5)]):

        pop = np.empty((npop, 3), dtype='object')
        xmin, xmax = bounds[0]
        ymin, ymax = bounds[1]

        for i in range(npop):
            pop[i, 0] = np.random.uniform(low=xmin, high=xmax)
            pop[i, 1] = np.random.uniform(low=xmin, high=xmax)

        self.initial_pop = pop
        self.npop = npop
        self.bounds = bounds

    def evolve(self, f, maxgen, eta, pc=0.9, pm=0.001, n_tourn=2):
        
        xmin, xmax = self.bounds[0]
        ymin, ymax = self.bounds[1]
        pop = self.initial_pop

        for i in range(self.npop):
            pop[i, 2] = f(pop[i, 0], pop[i, 1])

        # Inicializa a população selecionando valores aleatórios
        ngen = 0
        while ngen < maxgen:
            next_gen = np.empty((1, 3), dtype='object')[1::]

            # Preenche a próxima geração
            while next_gen.shape[0] < self.npop:

                # Utiliza torunament selection para criar o mating pool
                champions = []
                for l in range(2):
                    tourn = np.random.choice(range(self.npop), size=n_tourn, replace=False)
                    candidates = pop[tourn, :]
                    champions.append(candidates[np.argsort(candidates[:, 2])][0, [0, 1]])
                dad, mom = champions

                # Faz o crossover utilizando SXB
                if np.random.uniform(size=1) < pc:
                    u = np.random.uniform(size=1)
                    if u < 0.5:
                        beta = (2*u)**(1 / (eta + 1))
                    else:
                        beta = (1 / (2*(1 - u)))**(1 / (eta + 1))

                    offspring1 = []
                    offspring2 = []
                    for i in range(len(self.bounds)):
                        
                        var1 = 0.5*(1 + beta)*dad[i] + (1 - beta)*mom[i]
                        var2 = 0.5*(1 - beta)*dad[i] + (1 + beta)*mom[i]

                        ## Ajusta as variáveis que passarem dos limites estabelecidos
                        if var1 > self.bounds[i][1]:
                            var1 = self.bounds[i][1]
                        elif var1 < self.bounds[i][0]:
                            var1 = self.bounds[i][0]
                        
                        if var2 > self.bounds[i][1]:
                            var2 = self.bounds[i][1]
                        elif var2 < self.bounds[i][0]:
                            var2 = self.bounds[i][0]
                        
                        offspring1.append(var1)
                        offspring2.append(var2)

                    # o valor da fitness function ainda não é calculado
                    offspring1.append(0)
                    offspring2.append(0)

                    # Acrescenta o indivíduo a próxima geração
                    next_gen = np.vstack((next_gen, np.array(offspring1), np.array(offspring2)))
            
            # Realiza a mutação nos indivíduos da geração seguinte
            for i in range(next_gen.shape[0]):
                for j in range(next_gen.shape[1]):
                    if j == 2:
                        next_gen[i, j] = f(next_gen[i, 0], next_gen[i, 1])
                    else:
                        u = np.random.uniform(size=1)
                        if u < pm:
                            next_gen[i, j] = np.random.uniform(low=self.bounds[j][0], high=self.bounds[j][1])
                        else:
                            continue
            
            # Junta as duas populações e seleciona os npop-melhores indivíduos
            joined_pop = np.vstack((pop, next_gen))
            pop = joined_pop[np.argsort(joined_pop[:, 2])][range(self.npop), :]
            ngen += 1
        
        # Retorna a população final
        self.final_gen = pop