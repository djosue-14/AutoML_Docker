from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
from joblib import load
from config import Config
from preprocessing import load_preprocessor

# Configuración de la API
app = FastAPI(
    title="API de Predicción Lab 2",
    description="API del curso Product Development",
    version="1.0.0"
)

# Cargar el modelo y el preprocesador
model_path = f"models/{Config.MODEL.lower()}.pkl"
preprocessor_path = "models/preprocessor.pkl"

model = load(model_path)
preprocessor = load_preprocessor(preprocessor_path)

class PredictionInput(BaseModel):
    # AccountViewingInteraction: float = Field(..., description="Interacciones con la cuenta")
    # AverageViewingDuration: float = Field(..., description="Duración promedio de la visualización")
    # EngagementScore: float = Field(..., description="Puntuación")
    # ContentDownloadsPerMonth: float = Field(..., description="Descargas de contenido por mes")
    # MonthlyCharges: float = Field(..., description="Cargos mensuales")
    # AccountAge: float = Field(..., description="Antigüedad de la cuenta")
    # ViewingHoursPerWeek: float = Field(..., description="Horas de visualización por semana")
    # ViewingHoursVariation: float = Field(..., description="Variación en horas de visualización")
    # BandwidthUsage: float = Field(..., description="Uso de ancho de banda")
    # AnnualIncome: float = Field(..., description="Ingreso anual")
    # SupportTicketsPerMonth: float = Field(..., description="Tickets de soporte mensual")
    # UserRating: float = Field(..., description="Calificación del usuario")
    # NetworkLatency: float = Field(..., description="Latencia de red")
    # TotalCharges: float = Field(..., description="Cargos totales")
    # CommentsOnContent: int = Field(..., description="Comentarios en contenido")
    # Age: int = Field(..., description="Edad del usuario")
    # SocialMediaInteractions: int = Field(..., description="Interacciones en redes sociales")
    # WatchlistSize: int = Field(..., description="Tamaño de la lista de seguimiento")
    # WebsiteVisitsPerWeek: int = Field(..., description="Visitas al sitio web por semana")
    # PersonalizedRecommendations: int = Field(..., description="Recomendaciones personalizadas")

    SubscriptionType: str = Field(..., description="Tipo de suscripción")
    PaymentMethod: str = Field(..., description="Método de pago")
    PaperlessBilling: str = Field(..., description="Facturación sin papel")
    ContentType: str = Field(..., description="Tipo de contenido")
    MultiDeviceAccess: str = Field(..., description="Acceso multidispositivo")
    DeviceRegistered: str = Field(..., description="Dispositivo registrado")
    GenrePreference: str = Field(..., description="Preferencia de género")
    Gender: str = Field(..., description="Género")
    ParentalControl: str = Field(..., description="Control parental")
    SubtitlesEnabled: str = Field(..., description="Subtítulos habilitados")
    Location: str = Field(..., description="Ubicación")
    EducationLevel: str = Field(..., description="Nivel educativo")
    TotalChargesCategory: str = Field(..., description="Categoría de cargos totales")
    MonthlyChargesChange: str = Field(..., description="Cambio de cargos mensuales")
    SubscriptionPaymentInteraction: str = Field(..., description="Interacción con el pago de suscripción")


# Modelo de respuesta
class PredictionOutput(BaseModel):
    predictions: list[dict[str, float]]


@app.post("/predict", response_model=PredictionOutput)
def predict(input_data: PredictionInput):
    # Convertir los datos de entrada a un DataFrame
    data_dict = input_data.dict()
    df = pd.DataFrame([data_dict])

    try:
        # Preprocesar los datos
        X = preprocessor.transform(df)

        # Realizar la predicción
        probabilities = model.predict_proba(X)

        # Clases del modelo
        #class_names = model.classes_
        #class_names = [str(class_name) for class_name in model.classes_]  # Convertir a cadenas
        class_names = [f"Clase{int(class_name)}" for class_name in model.classes_]


        # Preparar las predicciones
        predictions = [
            {class_name: float(prob) for class_name, prob in zip(class_names, sample_probs)}
            for sample_probs in probabilities
        ]

        # Construir la respuesta usando Pydantic
        response = PredictionOutput(predictions=predictions)
        return response

    except Exception as e:
        # Manejo de errores
        raise HTTPException(status_code=500, detail=f"Error durante la predicción: {e}")
    