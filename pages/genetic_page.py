import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import src.genetic as gen

def write():
    st.write('''
        # Genetic Algorithms
        ## Using genetic algorithms for optimization, with the following methodology

        ### Real Encoding
        * **Selection:** Tournament Selection
        * **Crossover:** SBX (Simulated Binary Crossover)
        
        ### Binary Encoding
        * **Code:** Binary N-bit encoding
        * **Selection:** Tournament Selection
        * **Crossover:** 2 Point Crossover
        * **Mutation Probability:** $\\frac{1}{npop\\sqrt(nbits)}$

        ### Available functions:

        $$f(x) = \\frac{10sin(x^2 + y^2)}{\\sqrt{x^2 + y^2}}$$
    '''
    )
    col1, col2 = st.beta_columns([2, 1])
    with col1:
        npop = st.slider('Choose the population size', 10, 1000, 500)
    with col2:    
        encoding = st.selectbox('Select variable encoding', ('real', 'binary'), index = 0, format_func = lambda x: x.title())
    
    if encoding == 'real':
        col3, col4 = st.beta_columns([1, 1])
        with col3:
            maxgen = st.number_input('Maximum number of generations', min_value = 1, max_value = 200, value = 20, step = 1)
        with col4:    
            n_tourn = st.number_input('Competitors in tournament selection', min_value = 2, max_value = 10, value = 2, step = 1)
        
        col5, col6, col7 = st.beta_columns([1, 1, 1])
        with col5:    
            pc = st.number_input('Crossover Probability', min_value = 0.0, max_value = 1.0, value = 0.9, step = .05)
        with col6:    
            pm = st.number_input('Mutation Probability', min_value = 0.0, max_value = .3, value = 0.001, step = .001, format="%.3f")
        with col7:    
            eta = st.number_input('Distribution index', min_value = .05, max_value = 1.0, value = .25, step = .05)

        st.write("Evolution:")
        with st.spinner("Running algorithm ..."):
            model = gen.GeneticReal()
            model.generate_pop(npop = npop)
            model.evolve(gen.func, maxgen, eta, pc = pc, pm = pm, n_tourn = n_tourn)
        df = pd.DataFrame(model.final_gen, columns = ['x', 'y', 'f']).astype('float64')

        with st.beta_container():
            plot = alt.Chart(df, height=500, width=600).mark_point().encode(
                x = 'x:Q', 
                y = 'y:Q', 
                tooltip = ['x', 'y', 'f']
            )
            st.altair_chart(plot)
    
    else:
        col3, col4, col5 = st.beta_columns(3)
        with col3:
            maxgen = st.number_input('Maximum number of generations', min_value = 1, max_value = 200, value = 20, step = 1)
        with col4:    
            pc = st.number_input('Crossover Probability', min_value = 0.0, max_value = 1.0, value = 0.9, step = .05)
        with col5:    
            n_tourn = st.number_input('Competitors in tournament selection', min_value = 2, max_value = 10, value = 2, step = 1)
        
        st.write("Evolution:")
        with st.spinner("Running algorithm ..."):
            model = gen.GeneticBinary()
            model.generate_pop(npop = npop)
            model.evolve(gen.func, maxgen, pc = pc, n_tourn = n_tourn)
        df = pd.DataFrame(model.final_gen, columns = ['x', 'y', 'f']).astype('float64')

        with st.beta_container():
            plot = alt.Chart(df, height=500, width=600).mark_point().encode(
                x = 'x:Q', 
                y = 'y:Q', 
                tooltip = ['x', 'y', 'f']
            )
            st.altair_chart(plot)

if __name__ == '__main__':
    write()