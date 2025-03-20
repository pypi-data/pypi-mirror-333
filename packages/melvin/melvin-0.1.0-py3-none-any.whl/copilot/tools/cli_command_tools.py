import click
from typing import Dict
from utils import _err, _log, run_command
from tecton.cli.cli import cli


def get_command_help(command, prefix="") -> Dict:
    """Recursively get help text for a command and its subcommands"""
    result = {
        "name": prefix + command.name if prefix else command.name,
        "help": command.help,
        "options": [],
    }

    # Get options
    ctx = click.Context(command)
    for param in command.get_params(ctx):
        opt_record = param.get_help_record(ctx)
        if opt_record:
            result["options"].append({"name": opt_record[0], "help": opt_record[1]})

    # Get subcommands if this is a group
    if isinstance(command, click.Group):
        result["commands"] = []
        for cmd_name, cmd in sorted(command.commands.items()):
            if not cmd.hidden:
                sub_prefix = (
                    f"{prefix}{command.name} " if prefix else f"{command.name} "
                )
                result["commands"].append(get_command_help(cmd, sub_prefix))

    return result


def tecton_cli_help() -> dict:
    """
    Query the tecton CLI to get a structured representation of all available commands and their options.
    Can be used to explore the CLI's functionality, including commands for checking user identity,
    managing workspaces, and cluster connectivity.

    Returns:
        dict: A nested dictionary containing the CLI command structure with the following keys:
            - name (str): The command name
            - help (str): The command's help text
            - options (list): List of dictionaries containing option names and help text
            - commands (list): List of nested command dictionaries (for subcommands)
    """
    return get_command_help(cli)


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
