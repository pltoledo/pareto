import streamlit as st
import numpy as np
from src.base import BaseEvolver
from src.ops.selection import Selector
from src.ops.crossover import two_point_crossover, sbx_crossover
from src.ops.mutation import binary_mutation, real_mutation
from src.utils import decode


class BinaryEvolver(BaseEvolver):

    def __init__(self):
        pass
    
    def generate_pop(self, npop, nbits=10, bounds=[(-5, 5), (-5,  5)]):
        
        pop = np.empty((npop, 3), dtype = 'object')
        for i in range(npop):
            pop[i, 0] = ''.join([str(j) for j in np.random.randint(0, 2, nbits)])
            pop[i, 1] = ''.join([str(j) for j in np.random.randint(0, 2, nbits)])
        self.initial_pop = pop
        self.npop = npop
        self.nbits = nbits
        self.bounds = bounds

    def evolve(self, f, maxgen, selec_method = 'tournament', pc=0.9, n_candidates=2):

        pop = self.initial_pop
        for i in range(self.npop):
            pop[i, 2] = f(decode(pop[i, 0], self.bounds[0]), decode(pop[i, 1], self.bounds[1]))
        pm = 1 / (self.npop * np.sqrt(self.nbits)) # Probabilidade de mutação
        ngen = 0
        selector = Selector(selec_method)
        while ngen < maxgen:
            next_gen = np.empty((1, 3), dtype='object')[1::]
            # Preenche a próxima geração
            while next_gen.shape[0] < self.npop:
                # Faz o crossover utilizando 2 point crossover
                if np.random.uniform(size=1) < pc:
                    # Utiliza torunament selection para criar o mating pool
                    dad, mom = selector.select(pop, n_candidates)
                    offspring1, offspring2 = two_point_crossover(dad, mom, self.bounds, self.nbits)
                    # Acrescenta o indivíduo a próxima geração
                    next_gen = np.vstack((next_gen, np.array(offspring1), np.array(offspring2)))       
            # Realiza a mutação nos indivíduos da geração seguinte
            next_gen = binary_mutation(next_gen, f, pm, self.bounds)
            # Junta as duas populações e seleciona os npop-melhores indivíduos
            joined_pop = np.vstack((pop, next_gen))
            pop = joined_pop[np.argsort(joined_pop[:, 2])][range(self.npop), :]
            ngen += 1
        # Retorna a população com os valores decodificados
        for i in range(self.npop):
            pop[i, 0] = decode(pop[i, 0], self.bounds[0])
            pop[i, 1] =  decode(pop[i, 1], self.bounds[1])
        self.final_gen = pop

class RealEvolver(BaseEvolver):

    def __init__(self):
        pass
    
    def generate_pop(self, npop, bounds=[(-5, 5), (-5,  5)]):

        pop = np.empty((npop, 3), dtype='object')
        xmin, xmax = bounds[0]
        ymin, ymax = bounds[1]
        for i in range(npop):
            pop[i, 0] = np.random.uniform(low=xmin, high=xmax)
            pop[i, 1] = np.random.uniform(low=ymin, high=ymax)
        self.initial_pop = pop
        self.npop = npop
        self.bounds = bounds

    def evolve(self, f, maxgen, eta, selec_method = 'tournament', pc=0.9, pm=0.001, n_candidates=2):

        pop = self.initial_pop
        for i in range(self.npop):
            pop[i, 2] = f(pop[i, 0], pop[i, 1])
        ngen = 0
        selector = Selector(selec_method)
        while ngen < maxgen:
            next_gen = np.empty((1, 3), dtype='object')[1::]
            # Preenche a próxima geração
            while next_gen.shape[0] < self.npop:
                # Faz o crossover utilizando SXB
                if np.random.uniform(size=1) < pc:
                    # Utiliza torunament selection para criar o mating pool
                    dad, mom = selector.select(pop, n_candidates)
                    offspring1, offspring2 = sbx_crossover(dad, mom, self.bounds, eta)
                    # Acrescenta o indivíduo a próxima geração
                    next_gen = np.vstack((next_gen, np.array(offspring1), np.array(offspring2)))
            # Realiza a mutação nos indivíduos da geração seguinte
            next_gen = real_mutation(next_gen, f, pm, self.bounds)
            # Junta as duas populações e seleciona os npop-melhores indivíduos
            joined_pop = np.vstack((pop, next_gen))
            pop = joined_pop[np.argsort(joined_pop[:, 2])][range(self.npop), :]
            ngen += 1
        # Retorna a população final
        self.final_gen = pop