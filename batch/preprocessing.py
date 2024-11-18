import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

def preprocess_data(data, target):

    numeric_features = data.select_dtypes(include=["int64", "float64"]).columns.drop(target)
    categorical_features = data.select_dtypes(include=["object", "category"]).columns

    numeric_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="mean")),
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ], remainder="passthrough")

    X = data.drop(columns=[target])
    y = data[target]
    return preprocessor, X, y

def save_preprocessor(preprocessor, filepath):
    joblib.dump(preprocessor, filepath)


def load_preprocessor(filepath):
    return joblib.load(filepath)

