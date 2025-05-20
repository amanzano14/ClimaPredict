import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d
import pandas as pd

def apply_methods(df):
    x = df.iloc[:, 0].values
    y = df.iloc[:, 1].values
    results = {}

    # Ajuste de curvas (ejemplo: polinomio de grado 2)
    coeffs = np.polyfit(x, y, 2)
    results['polyfit'] = coeffs.tolist()

    # Derivada numérica
    dy_dx = np.gradient(y, x)
    results['derivative'] = dy_dx.tolist()

    # Interpolación lineal
    interp_func = interp1d(x, y, kind='linear')
    x_new = np.linspace(min(x), max(x), 100)
    y_interp = interp_func(x_new)
    results['interpolation'] = y_interp.tolist()

    return results
