from flask import Flask, render_template, request, send_from_directory
import numpy as np
import matplotlib.pyplot as plt
import os
import uuid

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Carpeta donde se guardarán las imágenes generadas
UPLOAD_FOLDER = "static/img"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------------- RUTAS ----------------------

@app.route("/", methods=["GET"])
def index():
    """
    Página principal donde se muestra el formulario de entrada.
    """
    return render_template("index.html")

@app.route("/procesar", methods=["POST"])
def procesar():
    """
    Procesa los datos ingresados por el usuario aplicando el método numérico seleccionado.
    Genera gráficos con matplotlib y devuelve el resultado y la imagen generada.
    """
    datos = request.form["datos"]
    metodo = request.form["metodo"]
    imagen = None

    try:
        # Transformar los datos ingresados en un array de números
        valores = np.array([float(x.strip()) for x in datos.split(",")])
        x_vals = np.arange(len(valores))  # Índices como eje X

        # Crear el gráfico
        fig, ax = plt.subplots()
        ax.plot(x_vals, valores, label="Datos originales", marker="o")

        # Aplicar el método seleccionado
        if metodo == "interpolacion":
            resultado = aplicar_interpolacion(ax, x_vals, valores)

        elif metodo == "ajuste":
            resultado = aplicar_ajuste(ax, x_vals, valores)

        elif metodo == "derivada":
            resultado = aplicar_derivada(ax, x_vals, valores)

        elif metodo == "optimizacion":
            resultado = aplicar_optimizacion(ax, valores)

        else:
            resultado = "Método no reconocido."
            ax = None

        # Guardar la imagen si el gráfico fue generado
        if ax:
            ax.legend()
            img_name = f"{uuid.uuid4().hex}.png"
            img_path = os.path.join(UPLOAD_FOLDER, img_name)
            plt.savefig(img_path)
            plt.close(fig)
            imagen = img_name

    except Exception as e:
        resultado = f"Error: {str(e)}"

    return render_template("index.html", resultado=resultado, imagen=imagen)

@app.route("/static/img/<path:filename>")
def imagen(filename):
    """
    Permite acceder a las imágenes generadas por el sistema.
    """
    return send_from_directory(UPLOAD_FOLDER, filename)

# ---------------------- FUNCIONES MODULARES ----------------------

def aplicar_interpolacion(ax, x_vals, valores):
    """
    Aplica interpolación lineal a los datos y agrega la curva al gráfico.
    """
    x_interp = np.linspace(0, len(valores) - 1, 100)
    y_interp = np.interp(x_interp, x_vals, valores)
    ax.plot(x_interp, y_interp, label="Interpolación", linestyle="--")
    return "Interpolación generada correctamente."

def aplicar_ajuste(ax, x_vals, valores):
    """
    Ajusta un polinomio de segundo grado a los datos.
    """
    coef = np.polyfit(x_vals, valores, 2)
    poly = np.poly1d(coef)
    y_ajuste = poly(x_vals)
    ax.plot(x_vals, y_ajuste, label="Ajuste polinómico", linestyle="--")
    return f"Coeficientes del polinomio: {coef}"

def aplicar_derivada(ax, x_vals, valores):
    """
    Calcula la derivada numérica de los datos.
    """
    derivada = np.diff(valores)
    ax.plot(x_vals[:-1], derivada, label="Derivada", linestyle="--")
    return f"Derivadas: {derivada.tolist()}"

def aplicar_optimizacion(ax, valores):
    """
    Encuentra el valor mínimo y lo marca en el gráfico.
    """
    minimo = np.min(valores)
    ax.axhline(minimo, color="red", linestyle="--", label=f"Mínimo: {minimo}")
    return f"Valor mínimo: {minimo}"

# ---------------------- EJECUCIÓN ----------------------

if __name__ == "__main__":
    # Ejecuta la app en modo debug
    app.run(debug=True)
