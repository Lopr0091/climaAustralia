# utils/predict.py

import pandas as pd
import joblib

def predecir_rainfall(ruta_csv, modelo_path="data/06_models/random_forest_regresion.pkl"):
    # Cargar datos
    X_nuevo = pd.read_csv(ruta_csv)

    # Cargar modelo
    modelo = joblib.load(modelo_path)

    # Predecir
    predicciones = modelo.predict(X_nuevo)
    return predicciones.tolist()
