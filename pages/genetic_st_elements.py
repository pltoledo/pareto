import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import src.genetic as gen
from src.functions import func_ref
from src.utils import func_text_st

def function_inputs():
    selec_func = st.selectbox('Select a function', ('base', 'rosenbrock', 'ackley', 'himmelblau'), index = 0, format_func = lambda x: x.title())
    func_text_st(selec_func)
    func = func_ref[selec_func]['callable']
    bounds = func_ref[selec_func]['bounds']
    return (selec_func, func, bounds)

def base_inputs():
    col1, col2 = st.beta_columns([2, 1])
    with col1:
        npop = st.slider('Choose the population size', 10, 1000, 500)
    with col2:    
        encoding = st.selectbox('Select variable encoding', ('real', 'binary'), index = 0, format_func = lambda x: x.title())
    return (npop, encoding)

def real_inputs(func, npop):
    col3, col4 = st.beta_columns([1, 1])
    with col3:
        maxgen = st.number_input('Maximum number of generations', min_value = 1, max_value = 1000, value = 20, step = 5)
    with col4:    
        n_candidates = st.number_input('Competitors in tournament selection', min_value = 2, max_value = 20, value = 2, step = 1)
    
    col5, col6, col7 = st.beta_columns([1, 1, 1])
    with col5:    
        pc = st.number_input('Crossover Probability', min_value = 0.0, max_value = 1.0, value = 0.9, step = .05)
    with col6:    
        pm = st.number_input('Mutation Probability', min_value = 0.0, max_value = .3, value = 0.001, step = .001, format="%.3f")
    with col7:    
        eta = st.number_input('Distribution index', min_value = .05, max_value = 1.0, value = .25, step = .05)
    return (maxgen, n_candidates, pc, pm, eta)

def binary_inputs(func, npop):
    col3, col4, = st.beta_columns(2)
    with col3:
        maxgen = st.number_input('Maximum number of generations', min_value = 1, max_value = 1000, value = 20, step = 1)
    with col4:    
        nbits = st.number_input('Number of Enconding Bits', min_value = 5, max_value = 100, value = 10, step = 1)
    col5, col6 = st.beta_columns(2)
    with col5:    
        pc = st.number_input('Crossover Probability', min_value = 0.0, max_value = 1.0, value = 0.9, step = .05)
    with col6:    
        n_candidates = st.number_input('Competitors in tournament selection', min_value = 2, max_value = 20, value = 2, step = 1)
    return (maxgen, n_candidates, pc, nbits)

def plot_pop(df):
    with st.beta_container():
        plot = alt.Chart(df, height=500, width=600).mark_point().encode(
            x = 'x:Q', 
            y = 'y:Q', 
            tooltip = ['x', 'y', 'f']
        )
        st.altair_chart(plot)

def compare_results(selec_func, df):
    teor_result = func_ref[selec_func]['minima']
    best_result = np.round(np.min(df['f']), 6)
    #try:
    #    abs_diff = teor_result - best_result 
    #except:
    #    abs_diff = '-'
    col_teor, col_result = st.beta_columns(2)
    with col_teor:
        st.write(f'Theoretical Result: {teor_result}')
    with col_result:
        st.write(f'Best Result: {best_result}')
    #with col_error:
    #    st.write(f'Absolute Difference: {abs_diff}')