import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

def decode(string, min, max):
    value = int(string, 2)
    return (((max - min) / (2**len(string) - 1)) * value) + min

def func(x, y):
    return (10 * np.sin(np.sqrt(x**2 + y**2))) / (np.sqrt(x**2 + y**2))

def genetic_opt(f: callable, npop: int, maxgen: int, nbits: int = 10, pc = 0.9, xmin: int = -5, xmax: int = 5, ymin: int = -5, ymax: int = 5, n_tourn = 5):
    
    pm = 1 / (npop * np.sqrt(nbits)) # Probabilida de mutação

    # Inicializa a população selecionando valores aleatórios
    pop = np.empty((npop, 3), dtype = 'object')
    for i in range(npop):
        pop[i, 0] = ''.join([str(j) for j in np.random.randint(0, 2, nbits)])
        pop[i, 1] = ''.join([str(j) for j in np.random.randint(0, 2, nbits)])
        pop[i, 2] = f(decode(pop[i, 0], xmin, xmax), decode(pop[i, 1], ymin, ymax))
    
    ngen = 0
    while ngen < maxgen:
        next_gen = np.empty((1, 3), dtype = 'object')[1::]

        # Preenche a próxima geração
        while next_gen.shape[0] < npop:

            # Utiliza torunament selection para criar o mating pool
            champions = []
            for l in range(2):
                tourn = np.random.choice(range(npop), size = n_tourn, replace = False)
                candidates = pop[tourn, :]
                champions.append(candidates[np.argsort(candidates[:, 2])][0, [0, 1]])
            dad, mom = champions

            # Faz o crossover utilizando 2 point crossover
            if np.random.uniform(size = 1) < pc:
                offspring1 = []
                offspring2 = []
                for i in range(2):
                    first_cpoint = np.random.randint(0, nbits, size = 1)[0]
                    if first_cpoint == nbits - 1:
                        second_cpoint = first_cpoint
                        first_cpoint = np.random.randint(0, second_cpoint, size = 1)[0]
                    else:
                        second_cpoint = np.random.randint(first_cpoint + 1, nbits, size = 1)[0]

                    var1 = dad[i][:first_cpoint] + mom[i][first_cpoint:second_cpoint] + dad[i][second_cpoint:]
                    var2 = mom[i][:first_cpoint] + dad[i][first_cpoint:second_cpoint] + mom[i][second_cpoint:]

                    ## Ajusta as variáveis que passarem dos limites estabelecidos
                    if decode(var1, xmin, xmax) > xmax:
                        var1 = '1111111111'
                    elif decode(var1, xmin, xmax) < xmin:
                        var1 = '0000000000'
                    
                    if decode(var2, ymin, ymax) > ymax:
                        var2 = '1111111111'
                    elif decode(var2, ymin, ymax) < ymin:
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
        pop = joined_pop[np.argsort(joined_pop[:, 2])][range(npop), :]
        ngen += 1
    
    # Retorna a população com os valores decodificados
    for i in range(npop):
        pop[i, 0] = decode(pop[i, 0], xmin, xmax)
        pop[i, 1] =  decode(pop[i, 1], ymin, ymax)
    return pop


def write():
    st.write('''
        # Genetic Algorithms
        ### Using genetic algorithms for optimization, with the following methodology

        * **Code:** Binary N-bit encoding
        * **Selection:** Tournament Selection
        * **Crossover:** 2 Point Crossover
        * **Mutation Probability:** $\\frac{1}{npop\\sqrt(nbits)}$

        ### Optmized function:

        $$f(x) = \\frac{10sin(x^2 + y^2)}{\\sqrt{x^2 + y^2}}$$
    '''
    )
    npop = st.slider('Choose the population size', 10, 1000, 500)
    col1, col2, col3 = st.beta_columns(3)

    with col1:
        maxgen = st.number_input('Maximum number of generations', min_value = 1, max_value = 200, value = 20, step = 1)
    with col2:    
        pc = st.number_input('Crossover Probability', min_value = 0.0, max_value = 1.0, value = 0.9, step = .05)
    with col3:    
        n_tourn = st.number_input('Competitors in tournament selection', min_value = 2, max_value = 10, value = 2, step = 1)

    st.write("Evolution:")
    with st.spinner("Running algorithm ..."):
        result = genetic_opt(func, npop, maxgen, pc = pc, n_tourn = n_tourn)
    df = pd.DataFrame(result, columns = ['x', 'y', 'f']).astype('float64')




    with st.beta_container():
        plot = alt.Chart(df, height=500, width=600).mark_point().encode(
            x = 'x:Q', 
            y = 'y:Q', 
            tooltip = ['x', 'y', 'f']
        )
        st.altair_chart(plot)

if __name__ == 'main':
    write()