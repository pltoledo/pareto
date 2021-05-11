import streamlit as st

def decode(string, min, max):
        value = int(string, 2)
        return (((max - min) / (2**len(string) - 1)) * value) + min

def func_text_st(selec_func):
    if selec_func == 'base':
        st.write('''
                Function: $f(x, y) = \\frac{10sin(x^2 + y^2)}{\\sqrt{x^2 + y^2}}$

                Minima: -

                Ilustration:
                '''
        )
        st.image('images/base.png')
    elif selec_func == 'rosenbrock':
        st.write('''
                Function: $f(x, y) = (a - x)^2 + b(y - x^2)^2$

                Minima: $(x, y) = (a, a^2)$

                Ilustration:
                '''
        )
        st.image('images/rosenbrock.png')