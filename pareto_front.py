import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

def pareto_front(n: int) -> tuple:
    x = np.random.uniform(size = n)
    y = np.random.uniform(size = n)
    order = np.argsort(x)
    pareto_opitimal = [order[0]]
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

st.write('''
# Finding the Pareto Front in 2-D Spaces
Finding the best solutions available for minimizing x and y
''')

n = st.slider('Choose the sample size', 10, 10000, 100)

st.write("Here's an example:")
x, y, classe = pareto_front(n)
df = pd.DataFrame([(i, j, k) for i, j, k in zip(x, y, classe)], columns = ['x', 'y', 'classe'])
plot = alt.Chart(df).mark_point().encode(
    x = 'x:Q', 
    y = 'y:Q', 
    color = alt.Color('classe', scale=alt.Scale(scheme='set1')),
    fill = alt.Color('classe', scale=alt.Scale(scheme='set1')), 
    tooltip = ['x', 'y']
)

st.altair_chart(plot, use_container_width=True)
