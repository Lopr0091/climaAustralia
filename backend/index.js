const express = require("express"); //Crea servidores en node.js es el equvialente a flask en python
const mysql = require("mysql"); //Para conexiones SQL

const app = express(); //Para el servidor
const puerto = 3000; //Para el Puerto es mejor usar 3000 o 3005

const conexion = mysql.createConnection({
  host: "192.168.144.1",
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

app.get("/predicciones", (req, res) => {//Define /predicciones
  conexion.query("SELECT * FROM predicciones_clima ORDER BY id_prediccion DESC", (error, resultados) => {
    if (error) {
      console.error("Error al hacer la consulta:", error);
      res.status(500).send("Error en la consulta");
      return;
    }
    res.json(resultados);
  });
});

app.listen(puerto, () => {
  console.log(`Servidor escuchando en http://localhost:${puerto}`);
});