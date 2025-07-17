require("dotenv").config();

const express = require("express");
const mysql = require("mysql2");
const path = require("path");

const app = express();
const puerto = process.env.PORT || 8080;

const conexion = mysql.createConnection({
  host: process.env.MYSQLHOST,
  user: process.env.MYSQLUSER,
  password: process.env.MYSQLPASSWORD,
  database: process.env.MYSQLDATABASE,
  port: process.env.MYSQLPORT
});

conexion.connect(error => {
  if (error) {
    console.error("Error al conectar a la base de datos:", error);
    return;
  }
  console.log("Conexión a MySQL establecida.");
});

app.get("/", (req, res) => {
  res.send("Servidor activo"); // Temporalmente, reemplaza el sendFile
});

app.get("/prediccion-hoy", (req, res) => {
  const hoy = new Date().toISOString().split("T")[0];

  const query = `
    SELECT PrediccionRainTomorrow, Rainfall 
    FROM predicciones_clima 
    WHERE Fecha = ?
    ORDER BY id_prediccion DESC 
    LIMIT 1
  `;

  conexion.query(query, [hoy], (error, resultados) => {
    if (error) {
      console.error("Error al consultar la predicción de hoy:", error);
      return res.status(500).json({ error: "Error en la base de datos" });
    }

    if (resultados.length === 0) {
      return res.json({ llueve: null, rainfall: null });
    }

    const prediccion = resultados[0].PrediccionRainTomorrow;
    const rainfall = resultados[0].Rainfall;
    res.json({ llueve: prediccion === "Yes", rainfall });
  });
});

app.listen(puerto, () => {
  console.log(`Servidor escuchando en puerto ${puerto}`);
});
