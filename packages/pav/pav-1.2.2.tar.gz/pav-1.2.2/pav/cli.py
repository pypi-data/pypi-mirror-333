from os import chdir

import click
from pathlib import Path

from .utils import activate_venv_and_run, get_python_command, get_venv_path


def venv_path_option(func):
    """A decorator for common and same options for venv path"""
    func = click.option(
        "-v", "--venv-path",
        type=click.Path(exists=True, file_okay=False, dir_okay=True),
        help="Path to the venv directory"
    )(func)
    return func


@click.group()
def main():
    pass


@main.command()
@venv_path_option
@click.option(
    "-a", "--arguments",
    type=click.STRING,
    help="Specify additional arguments to pass to the Python file during execution. "
         "Use quotes for multiple arguments or arguments containing spaces. "
         "For example: --arguments=\"-a 42 --verbose\""
)
@click.argument(
    "file_path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
def file(file_path: str, venv_path: str | None, arguments: str | None):
    """Execute Python file"""

    if not file_path.endswith(".py"):
        raise click.BadParameter("File extension must be .py")

    current_dir = Path.cwd()  # Get the current directory
    file_path = (current_dir / file_path).resolve()
    file_dir = file_path.parent  # Get the file directory

    # Specify venv path
    if venv_path is None:
        if (file_dir / "venv").exists():
            venv_path = file_dir / "venv"
        elif (current_dir / "venv").exists():
            venv_path = current_dir / "venv"
    else:
        venv_path = Path(venv_path)

    # Activate venv and run Python file
    activate_venv_and_run(
        f"{get_python_command()} {file_path} {arguments if arguments is not None else ''}",
        venv_path,
        file_dir
    )


@main.command()
@venv_path_option
@click.argument("cmd")
def command(cmd: str, venv_path: str | None):
    """Execute a shell command"""

    venv_path = get_venv_path(venv_path)
    activate_venv_and_run(cmd, venv_path)


@main.command()
@venv_path_option
@click.option(
    "-w", "--workdir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Change the working directory before executing commands"
)
def shell(venv_path: str | None, workdir: str | None):
    """Open shell to execute commands (To exit shell, enter "exit")"""

    current_dir = Path.cwd()  # Get the current working directory
    if workdir is not None:
        chdir(workdir)  # Change the working directory
        working_dir = Path(workdir)

        # Specify venv path
        if venv_path is None:
            if (working_dir / "venv").exists():
                venv_path = working_dir / "venv"
            elif (current_dir / "venv").exists():
                venv_path = current_dir / "venv"
        else:
            venv_path = (current_dir / venv_path).resolve()
    else:
        venv_path = get_venv_path(venv_path)

    while True:
        cmd = input("> ")
        if cmd in "exit":
            break
        activate_venv_and_run(cmd, venv_path)


if __name__ == "__main__":
    main()
