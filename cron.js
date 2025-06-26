const { exec } = require("child_process"); //Es nativo de nodejs.  exec permite ejecutar comandos como en terminal
//Con child proces se ejecutan comandos del SO y externos
function ejecutarPython(script) {//Se prepara para recibir el nombre del archivo python
  return new Promise((resolve, reject) => {
    exec(`python3 ${script}`, (error, stdout, stderr) => {
      const timestamp = new Date().toLocaleString();
      if (error) {
        console.error(`[${timestamp}] Error ejecutando ${script}: ${error.message}`);
        reject(error);
      } else if (stderr) {
        console.error(`[${timestamp}] Stderr en ${script}: ${stderr}`);
        resolve();
      } else {
        console.log(`[${timestamp}] ${script} -> ${stdout.trim()}`);
        resolve();
      }
    });
  });
}
  //setInetrval es como un for infinito, pero con pausas tras iteraciones.
setInterval(async () => { // Función de JavaScript que ejecuta código repetitivamente
  try { //Donde van los archivos q deben ejecutarse
    await ejecutarPython("generar_dato.py");
    await ejecutarPython("insertar_prediccion.py");
  } catch (e) {
    console.error("Error en ciclo de cron:", e);
  }
}, 30000); // cada cuantos segundos
