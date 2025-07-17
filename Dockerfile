FROM node:18

# Python y pip
RUN apt update && apt install -y python3 python3-pip
WORKDIR /app

# Node
COPY backend/package*.json ./
RUN npm install


COPY backend/ .
COPY generar_dato.py .
COPY insertar_prediccion.py .

#  dependencias Python
RUN pip3 install mysql-connector-python pandas joblib scikit-learn

EXPOSE 8080

# Ejecutar cron.js y backend
CMD ["node", "cron.js"]
