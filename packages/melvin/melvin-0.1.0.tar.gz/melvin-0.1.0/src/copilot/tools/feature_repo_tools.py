import os
from typing import List
from utils import _err, _success, get_cwd, is_in_feature_repo, run_command
from constants import STARTING_DIR


def create_feature_repo(repo_name: str) -> str:
    """
    Create a Tecton feature repo

    Args:
        repo_name: The name of the feature repo

    Returns:
        str: The output of the command
    """
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


def find_tecton_feature_repositories() -> List[str]:
    """
    Find available tecton feature repositories (sometimes also just called tecton repos or feature repos)

    Returns:
        List[str]: A list of paths to available feature repositories
    """
    tecton_folders = []

    for root, dirs, files in os.walk(os.getcwd()):
        if ".tecton" in files:
            tecton_folders.append(os.path.abspath(root))

    return tecton_folders
