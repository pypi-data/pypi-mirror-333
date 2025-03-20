from typing import Any, List

from constants import STARTING_DIR
from tecton import conf
from tecton._internals import metadata_service
from tecton_core.fco_container import FcoContainer
from tecton_proto.metadataservice.metadata_service__client_pb2 import (
    GetAllEntitiesRequest,
    GetAllFeatureServicesRequest,
    GetAllTransformationsRequest,
    GetAllVirtualDataSourcesRequest,
    GetTransformationRequest,
    ListWorkspacesRequest,
    QueryFeatureViewsRequest,
)
from utils import (
    _err,
    _log,
    _success,
    get_cwd,
    is_in_feature_repo,
    run_command,
    validate_syntax,
)


def create_feature_repo(repo_name: str) -> str:
    """
    Create a Tecton feature repo

    Args:

        repo_name: The name of the feature repo

    Returns:

        str: The output of the command
    """
    import os

    try:
        assert not is_in_feature_repo(), "You are already in a feature repo"

        cwd = get_cwd()
        repo_path = os.path.join(cwd, repo_name)
        os.makedirs(repo_path, exist_ok=False)
        os.chdir(repo_path)
        code, out, err = run_command("tecton init")
        if code == 0:
            return _success(
                f"{repo_name} created successfully, you are now in the repo: {repo_path}"
            )
        else:
            return _err(err)
    except Exception as e:
        return _err(e)


def move_to_folder(folder: str) -> str:
    """
    Move to a folder, a folder may or may not be a feature repo

    Args:

        folder: relative path or absolute path of the folder, if folder is empty, it will move back to the directory.

    Returns:

        str: whether the move is successful and whether it is a feature repo
    """
    import os

    try:
        if folder == "":
            os.chdir(STARTING_DIR)
            return _success("You are now in the starting directory " + STARTING_DIR)
        repo_path = os.path.abspath(folder)
        if not os.path.exists(repo_path):
            return _err(f"{repo_path} does not exist")
        if not os.path.isdir(repo_path):
            return _err(f"{repo_path} is not a directory")
        os.chdir(repo_path)
        is_fr = (
            "it is a feature repo"
            if is_in_feature_repo()
            else "it is not a feature repo"
        )
        return _success(f"You are now in {repo_path}, {is_fr}")
    except Exception as e:
        return _err(e)


def get_source_code_lineno() -> list[list[Any]]:
    """
    Get the python code (with line numbers starting from 1) for all data source and feature definitions

    Returns:

        list[list[str]]: The python code for all feature definitions,
            each element is also a list. It contains the line number as the first element
            and the code as the second element.
    """
    import os

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
    import os

    assert is_in_feature_repo(), "You must be in a feature repo"

    path = os.path.join(get_cwd(), "features.py")
    _log(":eyeglasses: Getting the source code from " + path)
    if not os.path.exists(path):
        return ""
    else:
        with open(path, "r") as f:
            return f.read()


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
    import os

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
            The summary should be under 100 words. If non-empty, it should start with "Previous problem: ". It should end with "(Gotcha identified)" if the problem was a gotcha.. It should end with "(tecton plan failed)" if tecton plan failed.

    Returns:

        str: The success or error message
    """
    import os

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
    return _success("Feature definitions updated without syntax issues")


def validate_code_change() -> str:
    """
    Validate the current feature code.

    Returns:

        str: The validation result
    """
    try:
        import os

        assert is_in_feature_repo(), "You must be in in a feature repo"
        _log(":question: Validating the code change")
        path = os.path.join(get_cwd(), "features.py")
        validate_syntax(path)
        code, out, err = run_command("tecton plan")
        if code == 0:
            return _success(
                "The code has been successfully validated via `tecton plan`. No issues found."
            )
        else:
            return _err(f"{err}\n\n{out}")
    except Exception as e:
        return _err(e)


def _modify_source_code(
    modifications: dict[int, str] = {},
    insertions: dict[int, list[str]] = {},
    deletions: dict[int, int] = {},
    explanation: str = "",
    revert_on_error: bool = False,
) -> str:
    src = None
    try:
        import os

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


def tecton_cli_help() -> str:
    """
    Query the tecton cli for all of the commands that you can run with it
    Can be used to figure out which user you're logged in as, which tecton workspaces you have access to, which cluster you're connected to (by calling get-caller-identity) etc.

    Returns:

        str: list of commands you can run with the tecton cli
    """
    try:
        _log("Query tecton cli for available commands")
        code, out, err = run_command("tecton")
        if code != 0:
            return _err(f"{err}\n\n{out}")
        return out
    except Exception as e:
        return _err(e)


def tecton_cli_execute(command: str = "") -> str:
    """
    Execute a tecton cli command
    Use the tecton_cli_help tool to figure out which commands you have at your disposal

    Args:

        command: tecton command to execute, including any flags for that command. Do not prefix with the name of the cli, tecton

    Returns:

        str: The result of the command. May indicate success or failure
    """
    try:
        _log(f"Running tecton cli command {command}")

        code, out, err = run_command(f"tecton {command}")
        if code != 0:
            return _err(f"{err}\n\n{out}")
        return out
    except Exception as e:
        return _err(e)


def find_tecton_feature_repositories() -> List[str]:
    """
    Find available tecton feature repositories (sometimes also just called tecton repos or feature repos)

    Returns:

        List[str]: A list of paths to available feature repositories
    """
    import os

    tecton_folders = []

    for root, dirs, files in os.walk(os.getcwd()):
        if ".tecton" in files:
            tecton_folders.append(os.path.abspath(root))

    return tecton_folders


def list_workspaces() -> List[str]:
    """
    List all workspaces in the currently connected Tecton cluster.

    Returns:
        List[str]: A list of workspace names in the connected Tecton cluster.
        Returns an empty list if the operation fails.
    """
    try:
        request = ListWorkspacesRequest()
        response = metadata_service.instance().ListWorkspaces(request)
        return [ws.name for ws in response.workspaces]
    except Exception as e:
        _err(f"Failed to list workspaces: {str(e)}")
        return []


def list_feature_views() -> List[dict]:
    """
    List all feature views in the currently connected tecton cluster

    Returns:
        List[dict]: A list of dictionaries containing name, description, workspace, and tags for each feature view
    """
    try:
        feature_views = []
        workspaces = list_workspaces()

        for workspace in workspaces:
            request = QueryFeatureViewsRequest(workspace=workspace)
            response = metadata_service.instance().QueryFeatureViews(request)

            for fco in response.fco_container.fcos:
                if hasattr(fco, "feature_view") and fco.feature_view.fco_metadata.name:
                    feature_views.append(
                        {
                            "name": fco.feature_view.fco_metadata.name,
                            "description": fco.feature_view.fco_metadata.description,
                            "workspace": workspace,
                            "tags": dict(fco.feature_view.fco_metadata.tags),
                        }
                    )

        return sorted(feature_views, key=lambda x: x["name"])
    except Exception as e:
        _err(f"Failed to list feature views: {str(e)}")
        return []


def list_feature_services() -> List[dict]:
    """
    List all feature services in the currently connected tecton cluster

    Returns:
        List[dict]: A list of dictionaries containing name, description, workspace, and tags for each feature service
    """
    try:
        feature_services = []
        workspaces = list_workspaces()

        for workspace in workspaces:
            request = GetAllFeatureServicesRequest(workspace=workspace)
            response = metadata_service.instance().GetAllFeatureServices(request)

            for feature_service in response.feature_services:
                if feature_service.fco_metadata.name:
                    feature_services.append(
                        {
                            "name": feature_service.fco_metadata.name,
                            "description": feature_service.fco_metadata.description,
                            "workspace": workspace,
                            "tags": dict(feature_service.fco_metadata.tags),
                        }
                    )

        return sorted(feature_services, key=lambda x: x["name"])
    except Exception as e:
        _err(f"Failed to list feature services: {str(e)}")
        return []


def list_transformations() -> List[dict]:
    """
    List all transformations in the currently connected tecton cluster

    Returns:
        List[dict]: A list of dictionaries containing name, description, workspace, and tags for each transformation
    """
    try:
        transformations = []
        workspaces = list_workspaces()

        for workspace in workspaces:
            request = GetAllTransformationsRequest(workspace=workspace)
            response = metadata_service.instance().GetAllTransformations(request)

            for transformation in response.transformations:
                if transformation.fco_metadata.name:
                    transformations.append(
                        {
                            "name": transformation.fco_metadata.name,
                            "description": transformation.fco_metadata.description,
                            "workspace": workspace,
                            "tags": dict(transformation.fco_metadata.tags),
                        }
                    )

        return sorted(transformations, key=lambda x: x["name"])
    except Exception as e:
        _err(f"Failed to list transformations: {str(e)}")
        return []


def get_feature_view_code(name: str, workspace: str) -> str:
    """
    Get the code definition of a feature view from the Tecton cluster.
    This essentially gets the transformation using the feature view name and assumes its the same name as transformation name which works in most cases.

    Args:
        name: The name of the feature view to retrieve
        workspace: The workspace containing the feature view

    Returns:
        str: The Python code definition of the feature view

    Raises:
        Exception: If the feature view is not found or other errors occur
    """
    try:
        request = GetTransformationRequest(
            name=name,
            workspace=workspace,
            run_object_version_check=not conf.get_bool("SKIP_OBJECT_VERSION_CHECK"),
        )
        response = metadata_service.instance().GetTransformation(request)
        fco_container = FcoContainer.from_proto(response.fco_container)
        transformation_spec = fco_container.get_single_root()

        if transformation_spec is None:
            msg = f"Transformation '{name}' not found in workspace '{workspace}'. Try running `list_feature_views()` to view all registered feature views."
            raise ValueError(msg)

        # Validate that all required fields are present
        if not hasattr(transformation_spec, "validation_args"):
            raise ValueError("Missing validation_args in transformation_spec")
        if not hasattr(transformation_spec.validation_args, "transformation"):
            raise ValueError("Missing transformation in validation_args")
        if not hasattr(transformation_spec.validation_args.transformation, "args"):
            raise ValueError("Missing args in transformation")
        if not hasattr(
            transformation_spec.validation_args.transformation.args, "user_function"
        ):
            raise ValueError("Missing user_function in args")
        if not hasattr(
            transformation_spec.validation_args.transformation.args.user_function,
            "body",
        ):
            raise ValueError("Missing body in user_function")

        return (
            transformation_spec.validation_args.transformation.args.user_function.body
        )
    except Exception as e:
        _err(f"Failed to get feature view code: {str(e)}")
        return ""


def list_data_sources() -> List[dict]:
    """
    List all data sources in the currently connected tecton cluster

    Returns:
        List[dict]: A list of dictionaries containing name, description, workspace, and tags for each data source
    """
    try:
        data_sources = []
        workspaces = list_workspaces()

        for workspace in workspaces:
            request = GetAllVirtualDataSourcesRequest(workspace=workspace)
            response = metadata_service.instance().GetAllVirtualDataSources(request)

            for data_source in response.virtual_data_sources:
                if data_source.fco_metadata.name:
                    data_sources.append(
                        {
                            "name": data_source.fco_metadata.name,
                            "description": data_source.fco_metadata.description,
                            "workspace": workspace,
                            "tags": dict(data_source.fco_metadata.tags),
                        }
                    )

        return sorted(data_sources, key=lambda x: x["name"])
    except Exception as e:
        _err(f"Failed to list data sources: {str(e)}")
        return []


def list_entities() -> List[dict]:
    """
    List all entities in the currently connected tecton cluster

    Returns:
        List[dict]: A list of dictionaries containing name, description, workspace, and tags for each entity
    """
    try:
        entities = []
        workspaces = list_workspaces()

        for workspace in workspaces:
            request = GetAllEntitiesRequest(workspace=workspace)
            response = metadata_service.instance().GetAllEntities(request)

            for entity in response.entities:
                if entity.fco_metadata.name:
                    entities.append(
                        {
                            "name": entity.fco_metadata.name,
                            "description": entity.fco_metadata.description,
                            "workspace": workspace,
                            "tags": dict(entity.fco_metadata.tags),
                        }
                    )

        return sorted(entities, key=lambda x: x["name"])
    except Exception as e:
        _err(f"Failed to list entities: {str(e)}")
        return []
