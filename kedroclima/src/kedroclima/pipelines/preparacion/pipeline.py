from kedro.pipeline import Pipeline, node, pipeline
from .nodes import preparar_datos

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preparar_datos,
                inputs="weather_raw",
                outputs="datos_preparados",
                name="node_preparar_datos",
            ),
        ]
    )
