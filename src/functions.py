import numpy as np
import math

def base(x, y):
    return (10 * np.sin(np.sqrt(x**2 + y**2))) / (np.sqrt(x**2 + y**2))

def rosenbrock(x, y, a=1, b=100):
    return (a - x)**2 + b*(y - x**2)**2

def ackley(x, y):
    return -20*np.exp(-.2*np.sqrt(.5*(x**2 + y**2))) - np.exp(.5*(np.cos(2*math.pi*x) + np.cos(2*math.pi*y))) + math.e + 20

def himmelblau(x, y):
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2

func_callables = {
    'base': base,
    'rosenbrock': rosenbrock,
    'ackley': ackley,
    'himmelblau': himmelblau
}

func_minimas  = {
    'base': '-',
    'rosenbrock': 0,
    'ackley': 0,
    'himmelblau': 0
}

#if selec_func == 'rosenbrock':
#    col_a, col_b = st.beta_columns(2)
#    with col_a:
#        a = st.number_input('Choose "a" constant',  min_value = 1, max_value = 50, value = 1, step = 1)
#    with col_b:    
#        b = st.number_input('Choose "b" constant',  min_value = 1, max_value = 1000, value = 100, step = 10)
#    func_args = {
#        'a': a,
#        'b': b
#    }