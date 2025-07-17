import random
import mysql.connector
from datetime import datetime, timedelta
import subprocess

def obtener_ip_gateway():
    result = subprocess.run(["ip", "route"], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if line.startswith("default via"):
            return line.split()[2]
    return "localhost"
ip_gateway = obtener_ip_gateway()

conexion = mysql.connector.connect(
    host="192.168.144.1", #o usar ip_gateway
    user="root",
    password="",
    database="clima_modelos"
)

import os

#conexion = mysql.connector.connect(
#    host=os.environ.get("DB_HOST", "localhost"),
#    user=os.environ.get("DB_USER", "root"),
#    password=os.environ.get("DB_PASSWORD", ""),
#    database=os.environ.get("DB_NAME", "clima_modelos")
#)

cursor = conexion.cursor()
cursor.execute("SELECT MAX(id), MAX(Fecha) FROM datos_climaticos")
ultimo_id, ultima_fecha = cursor.fetchone()
nuevo_id = (ultimo_id or 0) + 1
nueva_fecha = (ultima_fecha or datetime.today().date()) + timedelta(days=1)
direcciones = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
dato = (
    nuevo_id,
    nueva_fecha,
    'Sydney',
    round(random.uniform(5.0, 15.0), 1),      # MinTemp
    round(random.uniform(16.0, 35.0), 1),     # MaxTemp
    round(random.uniform(0.0, 20.0), 1),      # Rainfall
    round(random.uniform(1.0, 10.0), 1),      # Evaporation
    round(random.uniform(0.0, 12.0), 1),      # Sunshine
    random.choice(direcciones),              # WindGustDir
    round(random.uniform(20.0, 60.0), 1),     # WindGustSpeed
    random.choice(direcciones),              # WindDir9am
    random.choice(direcciones),              # WindDir3pm
    round(random.uniform(5.0, 30.0), 1),      # WindSpeed9am
    round(random.uniform(5.0, 30.0), 1),      # WindSpeed3pm
    round(random.uniform(30.0, 100.0), 1),    # Humidity9am
    round(random.uniform(30.0, 100.0), 1),    # Humidity3pm
    round(random.uniform(1005.0, 1025.0), 1), # Pressure9am
    round(random.uniform(1005.0, 1025.0), 1), # Pressure3pm
    random.randint(0, 8),                    # Cloud9am
    random.randint(0, 8),                    # Cloud3pm
    round(random.uniform(10.0, 25.0), 1),     # Temp9am
    round(random.uniform(15.0, 30.0), 1),     # Temp3pm
    random.choice(['Yes', 'No']),            # RainToday
    None,                                    # PrediccionRainTomorrow
    None,                                    # FechaPrediccion
    'simulado'                               # Fuente
)

# Insertar en la base de datos
query = """
    INSERT INTO datos_climaticos (
        id, Fecha, Location, MinTemp, MaxTemp, Rainfall, Evaporation, Sunshine,
        WindGustDir, WindGustSpeed, WindDir9am, WindDir3pm, WindSpeed9am,
        WindSpeed3pm, Humidity9am, Humidity3pm, Pressure9am, Pressure3pm,
        Cloud9am, Cloud3pm, Temp9am, Temp3pm, RainToday,
        PrediccionRainTomorrow, FechaPrediccion, Fuente
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
cursor.execute(query, dato)
conexion.commit()
cursor.close()
conexion.close()

print(f"Dato climático simulado insertado con ID {nuevo_id}.")
