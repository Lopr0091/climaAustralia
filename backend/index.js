const express = require("express"); // Crea servidores en Node.js
const mysql = require("mysql");     // Cliente MySQL original
const path = require("path");       // Para manejar rutas de archivos

const app = express();
const puerto = 3000;

const conexion = mysql.createConnection({
  host: "192.168.144.1",  // IP host 
  user: "root",
  password: "",
  database: "clima_modelos"
});

conexion.connect(error => {
  if (error) {
    console.error("Error al conectar a la base de datos:", error);
    return;
  }
  console.log("Conexión a MySQL establecida.");
});

app.use(express.static(path.join(__dirname)));

app.get("/predicciones", (req, res) => {
  conexion.query("SELECT * FROM predicciones_clima ORDER BY id_prediccion DESC", (error, resultados) => {
    if (error) {
      console.error("Error al hacer la consulta:", error);
      res.status(500).send("Error en la consulta");
      return;
    }
    res.json(resultados);
  });
});

app.get("/prediccion-reciente", (req, res) => {
  const query = `
    SELECT RainTomorrow_predicho AS llueve, 
           Rainfall_predicho AS rainfall, 
           fecha_prediccion AS fecha
    FROM predicciones_clima
    ORDER BY id_prediccion DESC
    LIMIT 1
  `;

  conexion.query(query, (error, resultados) => {
    if (error) {
      console.error("Error al consultar la predicción:", error);
      return res.status(500).json({ error: "Error en la base de datos" });
    }

    if (resultados.length === 0) {
      return res.json({ llueve: null, rainfall: null, fecha: null });
    }

    const { llueve, rainfall, fecha } = resultados[0];
    res.json({
      llueve: llueve === "Yes",
      rainfall: rainfall,
      fecha: fecha
    });
  });
});

app.listen(puerto, () => {
  console.log(`Servidor escuchando en http://localhost:${puerto}`);
});
