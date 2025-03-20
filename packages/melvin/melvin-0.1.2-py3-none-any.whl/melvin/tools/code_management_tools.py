import os
from typing import Any, List

from utils import (
    _err,
    _get_source_code,
    _log,
    _success,
    _code,
    get_cwd,
    is_in_feature_repo,
    run_command,
    validate_syntax,
)

# from tecton_utils import extract_tecton_objects


def get_source_code_lineno() -> List[List[Any]]:
    """
    Get the python code (with line numbers starting from 1) for all data source and feature definitions

    Returns:
        list[list[str]]: The python code for all feature definitions,
            each element is also a list. It contains the line number as the first element
            and the code as the second element.
    """
    assert is_in_feature_repo(), "You must be in a feature repo"

    path = os.path.join(get_cwd(), "features.py")
    if not os.path.exists(path):
        res = []
    else:
        with open(path, "r") as f:
            lines = f.read().splitlines()
            res = [[i + 1, line] for i, line in enumerate(lines)]
    if len(res) == 0:
        res = [[1, ""]]
    if res[-1][1] != "":
        res.append([len(res) + 1, ""])
    return res


def get_source_code() -> str:
    """
    Get the python source code of features.py

    Returns:

        str: The python code of features.py
    """
    assert is_in_feature_repo(), "You must be in a feature repo"

    path = os.path.join(get_cwd(), "features.py")
    _log(":eyeglasses: Getting the source code from " + path)
    return _get_source_code()


def modify_source_code(
    modifications: dict[int, str] = {},
    insertions: dict[int, list[str]] = {},
    deletions: dict[int, int] = {},
    explanation: str = "",
) -> str:
    """
    Modify the code of data source and feature definitions, before each call to this tool,
    get_source_code must be used to get the latest original code,
    so the delta change can be calculated based on that.

    Args:

        modifications: A dictionary with line number as key and the new code as value, provide empty dict if no modification
        insertions: A dictionary with insertion line number as key and a list of new lines as value, provide empty dict if no insertion
        deletions: A dictionary with start line number as key and count of lines to delete as value, provide empty dict if no deletion
        explanation: An explanation of the changes, in under 100 words

    Returns:

        str: a message indicating whether the change is successful

    Note:

        To modify the code, it is always helpful to search tecton documents.
    """
    return _modify_source_code(
        modifications=modifications,
        insertions=insertions,
        deletions=deletions,
        explanation=explanation,
        revert_on_error=False,
    )


def fix_syntax_issues(
    modifications: dict[int, str] = {},
    insertions: dict[int, list[str]] = {},
    deletions: dict[int, int] = {},
    explanation: str = "",
) -> str:
    """
    Modify the code to fix syntax issues.
    get_source_code must be used to get the latest original code,
    so the delta change can be calculated based on that.

    Args:

        modifications: A dictionary with line number as key and the new code as value, provide empty dict if no modification
        insertions: A dictionary with insertion line number as key and a list of new lines as value, provide empty dict if no insertion
        deletions: A dictionary with start line number as key and count of lines to delete as value, provide empty dict if no deletion
        explanation: An explanation of the changes, in under 100 words

    Returns:

        str: a message indicating whether the change is successful

    Note:

        If the modification caused new syntax error, the change will be reverted and you should retry.
    """
    path = os.path.join(get_cwd(), "features.py")
    try:
        validate_syntax(path)
        return _success("No syntax issues found")
    except SyntaxError:
        return _modify_source_code(
            modifications=modifications,
            insertions=insertions,
            deletions=deletions,
            explanation="Syntax fixer: " + explanation,
            revert_on_error=True,
        )
    except Exception as e:
        return _err(e)


def save_modified_code(
    python_code: str, explanation: str = "", previous_problem: str = ""
) -> str:
    """
    Save the new feature definition source code.
    The new code must be the whole content of the file.

    Args:

        python_code: The new python code for the features.py
        explanation: An explanation of the changes, in under 100 words
        previous_problem: A summary of the previous problem leading to this change. Set this to
            non-empty string only when the change is to fix an issure reported by a validation.
            The summary should be under 100 words. If non-empty, it should start with "Previous problem: "

    Returns:

        str: The success or error message
    """
    if previous_problem:
        _log(":exclamation: " + previous_problem)
    _log(":writing_hand: " + explanation)

    path = os.path.join(get_cwd(), "features.py")
    if not python_code.endswith("\n"):
        python_code += "\n"
    with open(path, "w") as f:
        f.write(python_code)
    try:
        validate_syntax(path)
        run_command(f"black {path}")
    except SyntaxError as se:
        return _err(se, prefix="Syntax error")
    finally:
        _code()
    return _success("Feature definitions updated without syntax issues")


def validate_with_tecton_plan() -> str:
    """
    Validate the current feature code using `tecton plan`

    Returns:

        str: The validation result
    """
    try:
        assert is_in_feature_repo(), "You must be in in a feature repo"
        _log(":question: Validating the code change")
        path = os.path.join(get_cwd(), "features.py")
        validate_syntax(path)
        # tecton_objects = extract_tecton_objects(path)
        code, out, err = run_command("tecton plan")
        if code == 0:
            return _success(
                "The code has been successfully validated via `tecton plan`. No issues found."
            )
        else:
            return _err(f"{err}\n\n{out}")
    except Exception as e:
        return _err(e)


def generate_flowchart_representation(
    nodes: list[str], edges: list[list[str]], types: list[str]
) -> str:
    """
    Generate a Tecton flowchart representation from the code or description in the context.
    It is for visualization purpose.

    Args:

        nodes: A list of node names
        edges: A list of edges, each edge must be a list of two node names in `nodes`
        types: A list of Tecton types, it must have the same length as `nodes`

    Returns:

        str: The flowchart representation.

    Note:

        - Each node must represent a Tecton object (e.g entity or feature view)
        - For a decorated function, node name is the functio name, and the type is the decorator name
        - The node names should be valid python identifiers
        - If there are errors, the return starts with "Error: "
        - The representation wiil ber surrounded by triple backticks, with the language set to "tecton_diagram"

    Example output:

    ```tecton_diagram
    {"rand_id": "gsdfg", "nodes": ["entity1", "feature_view1"], "edges": [["entity1", "feature_view1"]], "types": ["Entity", "BatchFeatureView"]}
    ```
    """
    import json
    import uuid

    rand_id = str(uuid.uuid4())[:5]

    repr = json.dumps(
        {"rand_id": rand_id, "nodes": nodes, "edges": edges, "types": types}
    )
    for edge in edges:
        if len(edge) != 2:
            return _err("Each edge must have two nodes: " + repr)
        if edge[0] not in nodes:
            return _err(f"Invalid source node {edge[0]} in an edge: " + repr)
        if edge[1] not in nodes:
            return _err(f"Invalid target node {edge[1]} in an edge: " + repr)
    return repr


def _modify_source_code(
    modifications: dict[int, str] = {},
    insertions: dict[int, list[str]] = {},
    deletions: dict[int, int] = {},
    explanation: str = "",
    revert_on_error: bool = False,
) -> str:
    src = None
    try:
        src = get_source_code_lineno()

        if explanation:
            _log(explanation)

        dels = set()
        for start, count in deletions.items():
            start = int(start)
            dels.update(range(start, start + count))
        modifications = {int(k): v for k, v in modifications.items()}
        insertions = {int(k): v for k, v in insertions.items()}
        res = []
        if 0 in insertions:
            res += insertions[0]
        for line, code in src:
            if line in modifications:
                res.append(modifications[line])
            elif line in insertions:
                res += insertions[line]
                if line not in dels:
                    res.append(code)
            else:
                if line not in dels:
                    res.append(code)
        while line + 1 in insertions:
            res += insertions[line + 1]
            line += 1
        path = os.path.join(get_cwd(), "features.py")
        with open(path, "w") as f:
            f.write("\n".join(res))
        validate_syntax(path)
        run_command(f"black {path}")
        return _success("Feature definitions updated without syntax issues")
    except SyntaxError as se:
        if revert_on_error:
            with open(path, "w") as f:
                f.write("\n".join([x[1] for x in src]))
            return _err(
                f"{se}, the change has been reverted, try again!", prefix="Syntax error"
            )
        else:
            return _err(se, prefix="Syntax error")
    except Exception as e:
        return _err(e)
    finally:
        _code()
