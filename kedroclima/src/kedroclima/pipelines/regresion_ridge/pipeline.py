from kedro.pipeline import Pipeline, node
from .nodes import entrenar_ridge_regresion

def create_pipeline(**kwargs):
    return Pipeline([
        node(
            func=entrenar_ridge_regresion,
            inputs=["X_train", "X_test", "y_train_regresion", "y_test_regresion"],
            outputs=["modelo_ridge_regresion", "reporte_ridge_regresion"],
            name="entrenar_ridge_regresion_node"
        )
    ])
