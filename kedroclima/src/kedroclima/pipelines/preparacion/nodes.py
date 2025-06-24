import pandas as pd

def preparar_datos(weather: pd.DataFrame) -> pd.DataFrame:
    df = weather.copy()

    # Proteger las columnas objetivo
    columnas_objetivo = ["RainTomorrow", "Rainfall"]

    # Separar numéricas y categóricas (sin las de objetivo)
    columnas_numericas = df.select_dtypes(include="number").columns.difference(columnas_objetivo)
    columnas_categoricas = df.select_dtypes(include="object").columns.difference(columnas_objetivo)

    # Porcentaje de nulos
    porcentaje_nulos = df.isnull().mean() * 100

    # 1. Eliminar FILAS con nulos en columnas poco importantes (< 9%)
    columnas_bajo_9 = porcentaje_nulos[porcentaje_nulos < 9].index.difference(columnas_objetivo)
    df.dropna(subset=columnas_bajo_9, inplace=True)

    # 2. Imputar columnas con ≥ 9% de nulos
    columnas_a_imputar = porcentaje_nulos[porcentaje_nulos >= 9].index.difference(columnas_objetivo)
    for col in columnas_a_imputar:
        if col in columnas_numericas:
            df[col] = df[col].fillna(df[col].mean())
        elif col in columnas_categoricas:
            df[col] = df[col].fillna(df[col].mode().iloc[0])

    # 3. Eliminar columnas dominadas por un solo valor (excepto las de objetivo)
    umbral_repeticion = 0.95
    columnas_dominadas = [
        col for col in df.columns.difference(columnas_objetivo)
        if df[col].value_counts(normalize=True).iloc[0] > umbral_repeticion
    ]
    df.drop(columns=columnas_dominadas, inplace=True)

    # 4. Eliminar outliers con IQR (solo en columnas numéricas sin objetivo)
    for col in columnas_numericas:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        limite_inferior = Q1 - 1.5 * IQR
        limite_superior = Q3 + 1.5 * IQR
        df = df[(df[col] >= limite_inferior) & (df[col] <= limite_superior)]

    return df
