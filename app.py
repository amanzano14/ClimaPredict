from flask import Flask, render_template, request, jsonify
import os
from utils.data_processing import parse_csv
from models.statistical_model import apply_methods
from plots.plot_generator import generate_plots

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    data = parse_csv(file)
    results = apply_methods(data)
    plot_paths = generate_plots(data)
    return jsonify({'results': results, 'plots': plot_paths})

if __name__ == '__main__':
    app.run(debug=True)
