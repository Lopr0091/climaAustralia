const { exec } = require("child_process");

function ejecutarPython(script) {
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

setInterval(async () => {
  try {
    await ejecutarPython("generar_dato.py");
    await ejecutarPython("insertar_prediccion.py");
  } catch (e) {
    console.error("Error en ciclo de cron:", e);
  }
}, 30000); // cada tantos segundos
