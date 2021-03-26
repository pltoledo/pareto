import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

def pareto_front(n: int, xobj:str = 'min', yobj: str = 'min') -> tuple:
    x = np.random.uniform(size = n)
    y = np.random.uniform(size = n)
    if xobj == 'max':
        order = np.argsort(x)[::-1]
    else:
        order = np.argsort(x)
    pareto_opitimal = [order[0]]
    if yobj == 'max':
        for index, value in enumerate(order):
            if index == 0:
                best_y = y[value]
            elif y[value] >= best_y:
                best_y = y[value]
                pareto_opitimal.append(value)
            else:
                continue
    else:
        for index, value in enumerate(order):
            if index == 0:
                best_y = y[value]
            elif y[value] <= best_y:
                best_y = y[value]
                pareto_opitimal.append(value)
            else:
                continue
    classification = np.repeat('Ponto Comum', n)
    classification[pareto_opitimal] = 'Pareto'
    return (x, y, np.array(classification))

'''
# Finding the Pareto Front in 2-D Spaces
Finding the best solutions available for minimizing x and y
'''

n = st.slider('Choose the sample size', 10, 1000, 100)
with st.beta_container():
    xobj = st.selectbox('Choose X objective', ['min', 'max'], index = 0, format_func = lambda x: x.title())
    yobj = st.selectbox('Choose Y objective', ['min', 'max'], index = 0, format_func = lambda x: x.title())

st.write("Here's what it looks like:")
x, y, classe = pareto_front(n, xobj = xobj, yobj = yobj)
df = pd.DataFrame([(i, j, k) for i, j, k in zip(x, y, classe)], columns = ['x', 'y', 'classe'])
plot = alt.Chart(df).mark_point().encode(
    x = 'x:Q', 
    y = 'y:Q', 
    color = alt.Color('classe', scale=alt.Scale(scheme='set1')),
    fill = alt.Color('classe', scale=alt.Scale(scheme='set1')), 
    tooltip = ['x', 'y']
)

st.altair_chart(plot, use_container_width=True)
