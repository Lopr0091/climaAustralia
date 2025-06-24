from kedro.pipeline import Pipeline, node
from .nodes import codificar_y_dividir

def create_pipeline(**kwargs):
    return Pipeline([
        node(
            func=codificar_y_dividir,
            inputs="datos_preparados",
            outputs=[
                "X_train",
                "X_test",
                "y_train_clasificacion",
                "y_test_clasificacion",
                "y_train_regresion",
                "y_test_regresion"
            ],
            name="codificar_y_dividir_node",
        )
    ])
