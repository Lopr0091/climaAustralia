from flask import Flask, request, jsonify
from utils.predict import predecir_rainfall

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No se encontró archivo"}), 400

    archivo = request.files['file']
    if archivo.filename == '':
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    try:
        archivo.save("temp.csv")
        resultados = predecir_rainfall("temp.csv")
        return jsonify({"predicciones": resultados})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
