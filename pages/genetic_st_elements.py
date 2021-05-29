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
        npop = st.slider('Population size', 10, 1000, 500)
    with col2:    
        maxgen = st.number_input('Maximum number of generations', min_value = 1, max_value = 1000, value = 20, step = 5)
    return (npop, maxgen)

def encoding_input():
    col1, col2 = st.beta_columns(2)
    with col1:
        encoding = st.selectbox('Type', ('real', 'binary'), index = 0, format_func = lambda x: x.title())
    if encoding == 'binary':
        with col2:
            nbits = st.number_input('Number of Bits', min_value = 5, max_value = 100, value = 10, step = 1)
        return (encoding, nbits)
    else:
        return encoding

def selector_inputs():
    methods = ['tournament', 'roulette']
    col1, col2 = st.beta_columns(2)
    with col1:
        selec_method = st.selectbox('Method', tuple(methods), index = 0, format_func = lambda x: x.title())
    if selec_method == 'tournament':
        with col2:
            n_candidates = st.number_input('Competitors in Tournament', min_value = 2, max_value = 20, value = 2, step = 1)
        selec_dict = dict(selec_method = selec_method, n_candidates = n_candidates)
        return selec_dict
    else:
        return dict(selec_method = selec_method)

def real_inputs(func, npop):
    col1, col2, col3 = st.beta_columns([1, 1, 1])
    with col1:    
        eta = st.number_input('Distribution Index', min_value = .05, max_value = 1.0, value = .25, step = .05)
    with col2:    
        pc = st.number_input('Crossover Probability', min_value = 0.0, max_value = 1.0, value = 0.9, step = .05)
    with col3:    
        pm = st.number_input('Mutation Probability', min_value = 0.0, max_value = .3, value = 0.001, step = .001, format="%.3f")
    return (eta, pc, pm)

def binary_inputs(func, npop):
    col3, col4, = st.beta_columns(2)
    with col3:    
        pc = st.number_input('Crossover Probability', min_value = 0.0, max_value = 1.0, value = 0.9, step = .05)
    return (pc)

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