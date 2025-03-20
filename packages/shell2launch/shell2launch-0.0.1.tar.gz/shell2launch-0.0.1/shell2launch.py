from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from pathlib import Path

__version__ = "0.0.1"


def _parse_args(shell_code: str) -> dict[str, list[str]]:
    """Parses the arguments of a python script call from shell code.

    Args:
        shell_code (str):
            The part of the shell script that invokes python. For example:
            python myprogram.py / --arg_one / --arg_two 1 / --arg_three 1 2 /

    Returns:
        dict[str, list[str]]:
            A dictionary that maps argument names two their values. In the
            above example:
            {"--arg_one": [], "--arg_two": ["1"], "--arg_three": ["1", "2"]}

    """
    shell_code = shell_code.replace("\\", "").replace("\n", "")
    shell_code_split = re.split("--|-", shell_code)
    positional_split = shell_code_split[0].split()
    optional_split = shell_code.split()

    arguments: dict[str, list[str]] = {}
    for positional in positional_split:
        arguments[positional] = []

    current_key = None

    for el in optional_split:
        if el.startswith("--") or el.startswith("-"):
            current_key = el
            arguments[current_key] = []
        elif current_key is not None:
            el = el[1:-1] if el.startswith('"') and el.endswith('"') else el
            arguments[current_key].append(el)

    return arguments


def _clean_shell_code(shell_code: str) -> str:
    """Removes commented lines as well as leading and trailing whitespaces

    Args:
        shell_code (str):
            The original shell code.

    Returns:
        str: The cleaned shell code.
    """
    cleaned = []
    for line in shell_code.splitlines():
        stripped_line = line.strip()
        if not stripped_line.startswith("#"):
            cleaned.append(stripped_line)
    return "\n".join(cleaned)


def _build_args_strings(args: dict[str, list[str]]) -> list[str]:
    """Builds a list of formatted argument strings.

    Args:
        args (dict[str, list[str]]):
            The arguments as a mapping of argument name to a list of provided
            values. The ouput of parse_args().

    Returns:
        list[str]:
            The "args": [...] part of the launch.json as a list of strings,
            one for each line in the launch.json.
    """
    args_strings = ['"args": [\n']
    for key, val in args.items():
        if len(val) > 0:
            val_string = '"' + '", "'.join(val) + '"'
            args_strings.append(f'\t"{key}", {val_string},\n')
        else:
            args_strings.append(f'\t"{key}",\n')

    args_strings.append("]")
    return args_strings


def _build_launch_string(python_filename: str, args: list[str]) -> str:
    """Returns a configuration entry for launch.json

    Args:
        python_filename (str):
            The name of the target python file, e.g. 'myprogram.py'
        args (list[str]):
            A list of the arguments the program should be invoked with.
            Contains both keys (e.g. '--myarg') and values (e.g. 'myvalue')

    Returns:
        str: The formatted debug configuration string.
    """
    launch_json = ["{\n"]
    launch_json.append(
        f'\t"name": "Python Debugger: {python_filename} with Arguments",\n'
    )
    launch_json.append('\t"type": "debugpy",\n')
    launch_json.append('\t"request": "launch",\n')
    launch_json.append(f'\t"program": "{python_filename}",\n')
    launch_json.append('\t"console": "integratedTerminal",\n')
    launch_json.extend(f"\t{x}" for x in args)
    launch_json.append("\n}")
    return "".join(launch_json)


def shell2launch(shell_code: str, args_only: bool = False) -> str:
    """Build a launch.json debug configuration based on shell code.

    Args:
        shell_code (str):
            Shell code that invokes a python script.
        args_only (bool, optional):
            If true, only return the "args": [...] part of the debug
            configuration. Defaults to False.

    Raises:
        ValueError: If the provided shell code does not invoke a python script
        via "python *.py"

    Returns:
        str: A formatted string for the launch.json debug configuration.
    """
    shell_code = _clean_shell_code(shell_code=shell_code)

    python_call_match = re.search(r"python .+\.py ", shell_code.strip())
    if python_call_match is not None:
        python_call = python_call_match.group()
    else:
        raise ValueError(
            "The provided bash string does not contain a '.py' file reference"
        )

    python_filename = python_call.split()[1]
    python_arguments = shell_code.split(python_call)[1].split("\n\n")[0]

    args = _parse_args(python_arguments)
    args_strings = _build_args_strings(args=args)

    if args_only:
        return "".join(args_strings)

    launch_json = _build_launch_string(python_filename, args_strings)
    return launch_json


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", type=str, help="path to the shell script")
    parser.add_argument(
        "-o",
        "--output_filepath",
        type=str,
        help="specify an output filepath to save the output",
    )
    parser.add_argument(
        "--args_only",
        action="store_true",
        help="only output the 'args: [...]' section of the launch configuration",
    )
    args = parser.parse_args(argv)

    with open(Path(args.filepath), "r") as f:
        shell_code = f.read()

    launch_json = shell2launch(shell_code=shell_code, args_only=args.args_only)

    if args.output_filepath is not None:
        Path(args.output_filepath).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output_filepath).touch(exist_ok=True)
        with open(args.output_filepath, "w") as f:
            f.write(launch_json)

    print(launch_json)
    return 0


if __name__ == "__main__":
    sys.exit(main())
