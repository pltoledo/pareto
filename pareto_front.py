import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

@st.cache
def get_values(n: int) -> tuple:
    x = np.random.uniform(size = n)
    y = np.random.uniform(size = n)
    return (x, y)

def pareto_front(x: np.array, y: np.array, xobj: str = 'min', yobj: str = 'min') -> np.array:
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
    classification = np.repeat('Non-Opitimal', n).astype('object')
    classification[pareto_opitimal] = 'Pareto Optimal'
    return np.array(classification)

'''
# Finding the Pareto Front in 2-D Spaces
Finding the best solutions available for minimizing x and y
'''

n = st.slider('Choose the sample size', 10, 1000, 100)
col1, col2 = st.beta_columns(2)
with col1:
    xobj = st.selectbox('Choose X objective', ['min', 'max'], index = 0, format_func = lambda x: x.title())
with col2:    
    yobj = st.selectbox('Choose Y objective', ['min', 'max'], index = 0, format_func = lambda x: x.title())

st.write("Here's what it looks like:")
x, y = get_values(n)
classe = pareto_front(x, y, xobj = xobj, yobj = yobj)
df = pd.DataFrame([(i, j, k) for i, j, k in zip(x, y, classe)], columns = ['x', 'y', 'classe'])

with st.beta_container():
    scatter = alt.Chart(df).mark_point().encode(
        x = 'x:Q', 
        y = 'y:Q', 
        color = alt.Color('classe', scale=alt.Scale(domain=['Non-Opitimal', 'Pareto Optimal'], range=["#377EB8", "#E41A1C"])),
        fill = alt.Color('classe', scale=alt.Scale(domain=['Non-Opitimal', 'Pareto Optimal'], range=["#377EB8", "#E41A1C"])),
        tooltip = ['x', 'y']
    )
    
    line = alt.Chart(df[df['classe'] == 'Pareto Optimal']).mark_line().encode(
                x = 'x:Q',
                y = 'y:Q',
            color = alt.Color('classe', scale=alt.Scale(domain=['Non-Opitimal', 'Pareto Optimal'], range=["#377EB8", "#E41A1C"])),
            tooltip = ['x', 'y']
        )
    plot = scatter + line

st.altair_chart(plot, use_container_width=True)
