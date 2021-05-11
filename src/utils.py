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
    elif selec_func == 'ackley':
        st.write('''
                Function: $f(x, y) = -20exp[-0.2\sqrt{0.5(x^2 + y^2)}] 
                                        - exp[0.5(cos2\pi{}x + cos2\pi{}y] + e + 20$

                Minima: $(x, y) = (0, 0)$

                Ilustration:
                '''
        )
        st.image('images/ackley.png')
    elif selec_func == 'himmelblau':
        st.write('''
                Function: $f(x, y) = (x^2 + y - 11)^2 + (x + y^2 - 7)^2$

                Minima: 
                * $(x, y) = (3.0, 2.0)$
                * $(x, y) = (-2.805118, 3.131312)$
                * $(x, y) = (-3.779310, -3.283186)$
                * $(x, y) = (3.584428, -1.848126)$

                Ilustration:
                '''
        )
        st.image('images/himmelblau.png')