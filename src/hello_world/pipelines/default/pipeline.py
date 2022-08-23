from kedro.pipeline import Pipeline, node, pipeline

from .nodes import return_greeting, join_statements


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=return_greeting,
                inputs=None,
                outputs="return-greet",
                name="define_greet",
            ),
            node(
                func=join_statements,
                inputs="return-greet",
                outputs=None,
                name="join_with_greet",
            ),
        ]
    )
