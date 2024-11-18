from automl import perform_hyperparameter_search
import pandas as pd
from config import Config
from preprocessing import preprocess_data
from preprocessing import save_preprocessor
import joblib

# Cargar los datos
data = pd.read_parquet(Config.DATASET)

preprocessor, X, y = preprocess_data(data, Config.TARGET)

preprocessor.fit(X)

save_preprocessor(preprocessor, "models/preprocessor.pkl")

X_transformed = preprocessor.transform(X)

best_model = perform_hyperparameter_search(Config.MODEL, X_transformed, y, Config.TRIALS)

joblib.dump(best_model, f'models/{Config.MODEL.lower()}.pkl')
