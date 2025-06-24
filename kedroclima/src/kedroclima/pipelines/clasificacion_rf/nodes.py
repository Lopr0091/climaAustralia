import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def entrenar_random_forest(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series
) -> tuple:
    modelo = RandomForestClassifier(random_state=42)
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)

    # Reporte de métricas
    reporte = classification_report(y_test, y_pred, output_dict=True)

    # Kedro guardará el modelo si lo retornamos
    return modelo, reporte
