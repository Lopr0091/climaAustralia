const mysql = require("mysql");
require("dotenv").config();

const conexion = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME
});

conexion.connect((err) => {
  if (err) {
    console.error("Error", err);
    return;
  }
  console.log("Conectado");

  const script = `
    CREATE TABLE IF NOT EXISTS datos_climaticos (
      id INT PRIMARY KEY,
      Fecha DATE,
      Location VARCHAR(50),
      MinTemp FLOAT,
      MaxTemp FLOAT,
      Rainfall FLOAT,
      Evaporation FLOAT,
      Sunshine FLOAT,
      WindGustDir VARCHAR(10),
      WindGustSpeed FLOAT,
      WindDir9am VARCHAR(10),
      WindDir3pm VARCHAR(10),
      WindSpeed9am FLOAT,
      WindSpeed3pm FLOAT,
      Humidity9am FLOAT,
      Humidity3pm FLOAT,
      Pressure9am FLOAT,
      Pressure3pm FLOAT,
      Cloud9am INT,
      Cloud3pm INT,
      Temp9am FLOAT,
      Temp3pm FLOAT,
      RainToday VARCHAR(3),
      PrediccionRainTomorrow VARCHAR(3),
      FechaPrediccion DATE,
      Fuente VARCHAR(50)
    );

    CREATE TABLE IF NOT EXISTS predicciones_clima (
      id_prediccion INT AUTO_INCREMENT PRIMARY KEY,
      Fecha DATE,
      Location VARCHAR(50),
      Rainfall FLOAT,
      PrediccionRainTomorrow VARCHAR(3),
      FechaGeneracion DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS metricas_modelo (
      id INT AUTO_INCREMENT PRIMARY KEY,
      nombre_modelo VARCHAR(50),
      accuracy FLOAT,
      precision FLOAT,
      recall FLOAT,
      f1_score FLOAT,
      fecha DATETIME DEFAULT CURRENT_TIMESTAMP
    );
  `;

  conexion.query(script, (err) => {
    if (err) {
      console.error("Error", err);
    } else {
      console.log("Tablas creadas.");
    }
    conexion.end();
  });
});
