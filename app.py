from flask import Flask, render_template, request, send_from_directory
import numpy as np
import matplotlib.pyplot as plt
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "static/img"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/procesar", methods=["POST"])
def procesar():
    datos = request.form["datos"]
    metodo = request.form["metodo"]
    imagen = None

    try:
        valores = np.array([float(x) for x in datos.split(",")])
        x_vals = np.arange(len(valores))

        fig, ax = plt.subplots()
        ax.plot(x_vals, valores, label="Datos originales", marker="o")

        if metodo == "interpolacion":
            x_interp = np.linspace(0, len(valores) - 1, 100)
            y_interp = np.interp(x_interp, x_vals, valores)
            ax.plot(x_interp, y_interp, label="Interpolación", linestyle="--")
            resultado = "Interpolación generada correctamente."

        elif metodo == "ajuste":
            coef = np.polyfit(x_vals, valores, 2)
            poly = np.poly1d(coef)
            y_ajuste = poly(x_vals)
            ax.plot(x_vals, y_ajuste, label="Ajuste polinómico", linestyle="--")
            resultado = f"Coeficientes del polinomio: {coef}"

        elif metodo == "derivada":
            derivada = np.diff(valores)
            ax.plot(x_vals[:-1], derivada, label="Derivada", linestyle="--")
            resultado = f"Derivadas: {derivada.tolist()}"

        elif metodo == "optimizacion":
            minimo = np.min(valores)
            ax.axhline(minimo, color="red", linestyle="--", label=f"Mínimo: {minimo}")
            resultado = f"Valor mínimo: {minimo}"

        else:
            resultado = "Método no reconocido."
            ax = None

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
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)
