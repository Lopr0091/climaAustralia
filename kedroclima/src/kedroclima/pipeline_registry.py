from __future__ import annotations

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
from kedroclima.pipelines import exploracion
from kedroclima.pipelines import preparacion
from kedroclima.pipelines.codificacion_split import pipeline as codificacion_split_pipeline
from kedroclima.pipelines.clasificacion_rf import pipeline as clasificacion_rf_pipeline
from kedroclima.pipelines.regresion_ridge import pipeline as regresion_ridge_pipeline

def register_pipelines() -> dict[str, Pipeline]:
    pipelines = find_pipelines()
    pipelines["exploracion"] = exploracion.create_pipeline()
    pipelines["preparacion"] = preparacion.create_pipeline()
    pipelines["codificacion_split"] = codificacion_split_pipeline.create_pipeline()
    pipelines["clasificacion_rf"] = clasificacion_rf_pipeline.create_pipeline()
    pipelines["regresion_ridge"] = regresion_ridge_pipeline.create_pipeline()
    pipelines["__default__"] = sum(pipelines.values())
    return pipelines
