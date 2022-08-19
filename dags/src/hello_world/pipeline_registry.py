"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline, pipeline
from hello_world.pipelines import default


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    hello_world_pipe = default.create_pipeline()
    return {"__default__": hello_world_pipe}
