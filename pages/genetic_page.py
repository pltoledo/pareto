import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import src.genetic as gen
from pages.genetic_st_elements import *

def write():
    # Algorithm Description
    st.write('''
        # Genetic Algorithms
        ## Using genetic algorithms for optimization, with the following methodology
        '''
    )
    col1, col2 = st.beta_columns(2)
    with col1:
        st.write('''
        ### Real Encoding
        * **Selection:** Tournament Selection
        * **Crossover:** SBX (Simulated Binary Crossover)
        '''
        )
    with col2:
         st.write('''
            ### Binary Encoding
            * **Code:** Binary N-bit encoding
            * **Selection:** Tournament Selection
            * **Crossover:** 2 Point Crossover
            * **Mutation Probability:** $\\frac{1}{npop\\sqrt(nbits)}$
         '''
         )
    # Define Initial Variables
    selec_func, func = function_inputs()
    npop, encoding = base_inputs()
    # Run Algorithm
    if encoding == 'real':
        maxgen, n_tourn, pc, pm, eta = real_inputs(func, npop)
        st.write("Evolution:")
        with st.spinner("Running algorithm ..."):
            evolver = gen.RealEvolver()
            evolver.generate_pop(npop = npop)
            evolver.evolve(func, maxgen, eta, pc = pc, pm = pm, n_tourn = n_tourn)
        df = pd.DataFrame(evolver.final_gen, columns = ['x', 'y', 'f']).astype('float64')
        plot_pop(df)
    else:
        maxgen, n_tourn, pc, nbits = binary_inputs(func, npop)
        st.write("Evolution:")
        with st.spinner("Running algorithm ..."):
            evolver = gen.BinaryEvolver()
            evolver.generate_pop(npop = npop, nbits=nbits)
            evolver.evolve(func, maxgen, pc = pc, n_tourn = n_tourn)
        df = pd.DataFrame(evolver.final_gen, columns = ['x', 'y', 'f']).astype('float64')
        plot_pop(df)
    # Analyze Interation Results
    compare_results(selec_func, df)

if __name__ == '__main__':
    write()