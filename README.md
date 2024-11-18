# AutoML_Docker

Este es un proyecto para la gestión de experimentación y modelos automatizados con Docker, con aplicaciones en FastAPI y Batch Processing.

## Link del repositorio
[Repositorio en Github](https://github.com/djosue-14/AutoML_Docker.git)

## Requisitos

Asegúrate de tener instaladas las siguientes dependencias en tu PC:

- Python 3.x
- Docker

Puedes instalar las dependencias necesarias utilizando pip:

```bash
pip install -r requirements.txt
```

Para la version FAST API debes configurar el archivo Dockerfile de esta manera

```bash
FROM python:3.12-slim

# Directorio de trabajo
WORKDIR /app

# Instalar requerimientos
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente y los modelos al contenedor
COPY ./src /app/src
COPY ./models /app/models

# Definir el PYTHONPATH
ENV PYTHONPATH=/app/src

# Exponer el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación FastAPI
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Luego debes construir la imagen y el contenedor de esta manera:

```bash
docker build -t api-lab2:latest .

docker run -d -p 8000:8000 --env-file .env api-lab2:latest
```

Luego consumir el API de esta manera:

[Localhost](http://localhost:8000/docs#/default/predict_predict_post)

Puedes utilizar estos valores para prueba:

```json
{
  "SubscriptionType": "Basic",
  "PaymentMethod": "Credit card",
  "PaperlessBilling": "Yes",
  "ContentType": "Movies",
  "MultiDeviceAccess": "No",
  "DeviceRegistered": "Tablet",
  "GenrePreference": "Action",
  "Gender": "Male",
  "ParentalControl": "No",
  "SubtitlesEnabled": "Yes",
  "Location": "Suburban",
  "EducationLevel": "Bachelor",
  "TotalChargesCategory": "Medium",
  "MonthlyChargesChange": "Decreased",
  "SubscriptionPaymentInteraction": "Basic-Credit card"
}
```

Para la version Batch debes configurar el archivo Dockerfile de esta manera

```bash
FROM python:3.12-slim

# Directorio de trabajo
WORKDIR /app

# Copiar los requerimientos y la carpeta batch
COPY requirements.txt /app/
COPY ./batch /app/batch
COPY ./models /app/models

# Instalar los requerimientos
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar el script Batch
CMD ["python", "batch/batch.py"]
```

Luego debes construir la imagen y el contenedor de esta manera:

```bash
docker build -t batch-lab2-app .

docker run --rm -v $(pwd)/data/input:/app/data/input -v $(pwd)/data/output:/app/data/output batch-lab2-app
```
