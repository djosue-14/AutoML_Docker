import os
import pandas as pd
from joblib import load
from config import Config
from preprocessing import load_preprocessor


def predict_batch(input_folder, output_folder, model_path):
    model = load(model_path)
    preprocessor = load_preprocessor("models/preprocessor.pkl")

    class_names = [f"Clase{int(class_name)}" for class_name in model.classes_]

    for file in os.listdir(input_folder):
        if file.endswith(".parquet"):
            data = pd.read_parquet(os.path.join(input_folder, file))
            
            try:
                X = preprocessor.transform(data)
                
                probabilities = model.predict_proba(X)
                
                predictions = [
                    {class_name: float(prob) for class_name, prob in zip(class_names, sample_probs)}
                    for sample_probs in probabilities
                ]
                
                output_df = pd.DataFrame(predictions)
                
                output_file_path = os.path.join(output_folder, f"predictions_{file}")
                output_df.to_parquet(output_file_path)
                print(f"Predicciones guardadas en: {output_file_path}")
            
            except Exception as e:
                print(f"Error procesando {file}: {e}")


if __name__ == "__main__":
    predict_batch(Config.INPUT_FOLDER, Config.OUTPUT_FOLDER, f"models/{Config.MODEL.lower()}.pkl")
