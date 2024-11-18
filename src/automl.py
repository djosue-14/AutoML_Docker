import optuna
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score

# Función para crear el modelo basado en el tipo especificado
def create_model(model_type, params):
    if model_type == "RandomForest":
        return RandomForestClassifier(**params)
    elif model_type == "GradientBoosting":
        return GradientBoostingClassifier(**params)
    elif model_type == "SVM":
        return SVC(**params)
    elif model_type == "KNN":
        return KNeighborsClassifier(**params)
    elif model_type == "NaiveBayes":
        return GaussianNB()
    else:
        raise ValueError(f"Modelo desconocido: {model_type}")

# Función para realizar la búsqueda de hiperparámetros con Optuna
def perform_hyperparameter_search(model_type, X_train, y_train, n_trials):
    def objective(trial):
        params = {}
        if model_type == "RandomForest":
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 10, 50),
                "max_depth": trial.suggest_int("max_depth", 3, 10),
                "min_samples_split": trial.suggest_int("min_samples_split", 2, 5),
            }
        elif model_type == "GradientBoosting":
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 10, 50),
                "learning_rate": trial.suggest_float("learning_rate", 0.05, 0.2),
                "max_depth": trial.suggest_int("max_depth", 3, 8),
            }
        elif model_type == "SVM":
            params = {
                "C": trial.suggest_float("C", 0.1, 5),
                "kernel": trial.suggest_categorical("kernel", ["linear"]),
                "max_iter": trial.suggest_int("max_iter", 100, 1000),  # Límite de iteraciones
            }
        elif model_type == "KNN":
            params = {
                "n_neighbors": trial.suggest_int("n_neighbors", 3, 10),
                "weights": trial.suggest_categorical("weights", ["uniform", "distance"]),
            }

        model = create_model(model_type, params)
        score = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy").mean()
        return score

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)

    print(f"Mejor conjunto de hiperparámetros: {study.best_params}")
    best_model = create_model(model_type, study.best_params)
    best_model.fit(X_train, y_train)
    return best_model
