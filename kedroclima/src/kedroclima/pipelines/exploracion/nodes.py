import pandas as pd

def explorar_weather(weather: pd.DataFrame) -> dict:
    return {
        "shape": weather.shape,
        "tipos_datos": weather.dtypes.astype(str).to_dict(),
        "porcentaje_nulos": (weather.isnull().mean() * 100).round(2).to_dict(),
        "valores_unicos": weather.nunique().to_dict(),
        "descripcion": weather.describe(include='all').to_dict()
    }
