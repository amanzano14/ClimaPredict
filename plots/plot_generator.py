import matplotlib.pyplot as plt
import numpy as np
import os

def generate_plots(df):
    x = df.iloc[:, 0].values
    y = df.iloc[:, 1].values
    plots = []

    # Original
    plt.figure()
    plt.plot(x, y, 'bo-', label='Original')
    plt.title('Datos Originales')
    plt.legend()
    path = 'static/original.png'
    plt.savefig(path)
    plots.append('/' + path)

    # Ajuste polinómico
    coeffs = np.polyfit(x, y, 2)
    poly = np.poly1d(coeffs)
    x_fit = np.linspace(min(x), max(x), 100)
    y_fit = poly(x_fit)
    plt.figure()
    plt.plot(x, y, 'bo')
    plt.plot(x_fit, y_fit, 'r-', label='Ajuste Cuadrático')
    plt.title('Ajuste de Curva')
    plt.legend()
    path = 'static/polyfit.png'
    plt.savefig(path)
    plots.append('/' + path)

    return plots
