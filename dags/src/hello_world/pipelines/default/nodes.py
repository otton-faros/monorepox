# Prepare first node
import logging
from tokenize import String


def return_greeting() -> String:
    return "Hello"


# Prepare second node
def join_statements(greeting):
    logger = logging.getLogger(__name__)
    logger.info(greeting + " Kedro!")
