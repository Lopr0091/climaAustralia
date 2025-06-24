import pandas as pd
import joblib
import mysql.connector
from datetime import datetime
import subprocess

def obtener_ip_gateway():
    result = subprocess.run(["ip", "route"], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.startswith("default via"):
            return line.split()[2]
    return "localhost"
ip_gateway = obtener_ip_gateway()

modelo_clasificacion = joblib.load("backend/data/06_models/random_forest_clasificacion.pkl")
modelo_regresion = joblib.load("backend/data/06_models/random_forest_regresion.pkl")


conexion = mysql.connector.connect(
    host="192.168.144.1", #o usar ip_gateway
    user="root",
    password="",
    database="clima_modelos"
)
cursor = conexion.cursor()
cursor.execute("SELECT * FROM datos_climaticos ORDER BY id DESC LIMIT 1")
columnas = [desc[0] for desc in cursor.description]
resultado = cursor.fetchone()

if not resultado:
    raise ValueError("No se encontraron datos en la tabla datos_climaticos")

# Crear DataFrame con el nuevo dato
nuevo_dato = pd.DataFrame([resultado], columns=columnas).drop(columns=["id"])

# Alinear columnas con el entrenamiento
X_train = pd.read_csv("kedroclima/data/05_model_input/X_train.csv")
columnas_entrenamiento = X_train.columns.tolist()

# Rellenar columnas faltantes con 0
for col in columnas_entrenamiento:
    if col not in nuevo_dato.columns:
        nuevo_dato[col] = 0
nuevo_dato = nuevo_dato[columnas_entrenamiento]

# Predicción
pred_clas = modelo_clasificacion.predict(nuevo_dato)[0]
pred_reg = modelo_regresion.predict(nuevo_dato)[0]

# Insertar predicción
cursor.execute("""
    INSERT INTO predicciones_clima (id_dato, RainTomorrow_predicho, Rainfall_predicho, fecha_prediccion)
    VALUES (%s, %s, %s, %s)
""", (resultado[columnas.index("id")], str(pred_clas), float(pred_reg), datetime.now()))

conexion.commit()
cursor.close()
conexion.close()

print("Predicción insertada correctamente.")
