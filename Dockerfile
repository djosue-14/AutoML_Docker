# # Base
# FROM python:3.12-slim

# # Directorio de trabajo
# WORKDIR /app

# RUN apt-get update && apt-get install -y \
#     gcc \
#     python3-dev \
#     && apt-get clean

# COPY requirements.txt /app/

# # Instalar requerimientos
# RUN pip install --no-cache-dir -r requirements.txt

# COPY ./src /app/src

# COPY ./models /app/models

# ENV PYTHONPATH=/app/src

# EXPOSE 8000

# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

COPY requirements.txt /app/

# Copia los archivos de tu proyecto al contenedor
COPY ./batch /app/batch
COPY ./models /app/models

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar el script batch
CMD ["python", "batch/batch.py"]
