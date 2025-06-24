import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

def codificar_y_dividir(datos: pd.DataFrame):
    df = datos.copy()

    # Eliminar columnas innecesarias
    columnas_a_eliminar = ["Date", "RISK_MM"]
    df = df.drop(columns=[col for col in columnas_a_eliminar if col in df.columns])

    # Objetivos
    y_clas = df["RainTomorrow"]
    y_reg = df["Rainfall"]

    # Eliminar columnas objetivo del input
    X = df.drop(columns=["RainTomorrow", "Rainfall"])

    # Separar categóricas
    cat_cols = X.select_dtypes(include=["object", "category"]).columns.tolist()

    # Codificar OneHot sobre TODO el dataset (no solo X_train)
    encoder = OneHotEncoder(sparse_output=False, handle_unknown="ignore")
    X_encoded = pd.DataFrame(encoder.fit_transform(X[cat_cols]))
    X_encoded.columns = encoder.get_feature_names_out(cat_cols)
    X_encoded.index = X.index

    # Combinar codificadas con numéricas
    X_numericas = X.drop(columns=cat_cols).reset_index(drop=True)
    X_encoded = X_encoded.reset_index(drop=True)
    X_final = pd.concat([X_numericas, X_encoded], axis=1)

    # Split (una sola vez para todo)
    X_train, X_test, y_train_clas, y_test_clas, y_train_reg, y_test_reg = train_test_split(
        X_final, y_clas, y_reg, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train_clas, y_test_clas, y_train_reg, y_test_reg
