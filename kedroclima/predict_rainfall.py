import pandas as pd
import joblib
import sys
import os

# Verificar cantidad de argumentos
if len(sys.argv) != 2:
    print("Uso: python predict_rainfall.py ruta_al_csv")
    sys.exit(1)

# Verificar que el archivo CSV exista
ruta_csv = sys.argv[1]
if not os.path.exists(ruta_csv):
    print(f"Error: El archivo '{ruta_csv}' no existe.")
    sys.exit(1)

# Cargar archivo de entrada
try:
    X_nuevo = pd.read_csv(ruta_csv)
except Exception as e:
    print(f"Error al leer el archivo CSV: {e}")
    sys.exit(1)

# Cargar modelo
modelo_path = "data/06_models/random_forest_regresion.pkl"
if not os.path.exists(modelo_path):
    print(f"Error: El modelo no se encontró en '{modelo_path}'.")
    sys.exit(1)

try:
    modelo = joblib.load(modelo_path)
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    sys.exit(1)

# Validar que las columnas coincidan
columnas_esperadas = modelo.feature_names_in_
if not all(col in X_nuevo.columns for col in columnas_esperadas):
    print("Error: El archivo CSV no contiene todas las columnas necesarias.")
    print("Se esperaban las columnas:")
    print(columnas_esperadas)
    print("Pero se encontraron:")
    print(X_nuevo.columns.tolist())
    sys.exit(1)

# Reordenar columnas por seguridad
X_nuevo = X_nuevo[columnas_esperadas]

# Hacer predicciones
try:
    predicciones = modelo.predict(X_nuevo)
except Exception as e:
    print(f"Error al hacer predicciones: {e}")
    sys.exit(1)

# Mostrar resultados
for i, p in enumerate(predicciones, 1):
    print(f"Fila {i}: {p:.2f} mm")
