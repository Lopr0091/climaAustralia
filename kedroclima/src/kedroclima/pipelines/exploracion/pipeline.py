from kedro.pipeline import Pipeline, node, pipeline
from .nodes import explorar_weather

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=explorar_weather,
            inputs="weather_raw",
            outputs="reporte_exploracion",
            name="nodo_exploracion"
        )
    ])
