import json
import logging
import os
import shutil
from tempfile import gettempdir
from typing import Any, Dict, Optional, Union

from ..utils._dev_utils import set_dev_flag


def set_dev_mode():
    """
    Set the dev mode for testing and local development. In dev mode, you
    don't need to connect to tecton.
    """
    set_dev_flag()
    os.environ["TECTON_SKIP_OBJECT_VALIDATION"] = "true"
    os.environ["TECTON_OFFLINE_RETRIEVAL_COMPUTE_MODE"] = "rift"
    os.environ["TECTON_BATCH_COMPUTE_MODE"] = "rift"
    os.environ["TECTON_FORCE_FUNCTION_SERIALIZATION"] = "false"
    os.environ["DUCKDB_EXTENSION_REPO"] = ""


def make_local_vector_db_config(
    path: Optional[str] = None, remove_if_exists: bool = True
) -> Dict[str, Any]:
    """
    Create a local vector db configuration for testing.

    Args:

        path: The path to the local vector db, defaults to None (system temp directory / test.db).
        remove_if_exists: Whether to remove the existing db file, defaults to True.

    Returns:

        Dict[str, Any]: The local vector db configuration

    Note:

        - The local vector db is a LanceDB with OpenAIEmbeddings, it requires Langchain to be installed.
        - You need an OpenAI API key to use OpenAIEmbeddings.
        - Specifying the path is recommended to avoid conflicts with other tests.
    """
    if path is None:
        _path = os.path.join(gettempdir(), "tecton_local_vector_db_for_test.db")
    else:
        _path = path
    if remove_if_exists:
        shutil.rmtree(_path, ignore_errors=True)

    return {
        "provider": "lancedb",
        "embedding": "openai/text-embedding-3-small",
        "uri": _path,
    }


def make_debug_logger(filter: Any = None) -> logging.Logger:
    """
    Create a logger for debugging.

    Args:

        filter: The filter functionto apply to the logger, defaults to None (no filter).

    Returns:

        logging.Logger: The logger

    Example:

        ```python
        from tecton_gen_ai.testing.utils import make_debug_logger

        logger = make_debug_logger(filter=lambda record: "invoking" in record.getMessage())
        ```
    """
    from rich.logging import RichHandler

    logger = logging.getLogger("rich_logger")
    logger.setLevel(logging.DEBUG)
    handler = RichHandler(show_time=False)
    logger.handlers.clear()
    logger.addHandler(handler)
    if filter is not None:
        logger.filters.clear()
        logger.addFilter(filter)
    return logger


def print_md(text: Union[dict[str, Any], str]) -> None:
    """
    Print markdown text in a rich format if rich is installed, otherwise use IPython.

    Args:

        text: The markdown text to print or a python dict
    """
    if isinstance(text, dict):
        md = json.dumps(text, indent=2)
    else:
        md = None
    try:
        import rich
        from rich.markdown import Markdown

        rich.print(md or Markdown(text))
    except ImportError:
        from IPython.display import Markdown, display

        display(md or Markdown(text))
