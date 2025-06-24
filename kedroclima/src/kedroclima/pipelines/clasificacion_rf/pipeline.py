from kedro.pipeline import Pipeline, node, pipeline
from .nodes import entrenar_random_forest

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=entrenar_random_forest,
            inputs=["X_train", "X_test", "y_train_clasificacion", "y_test_clasificacion"],
            outputs=["modelo_random_forest_clasificacion", "reporte_random_forest_clasificacion"],
            name="entrenar_random_forest_node",
        )
    ])
