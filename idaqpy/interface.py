import typing as t
from pathlib import Path

import typer
from idaqpy.utils import find_log_files, prompt_for_dir, prompt_for_file


idaq_cli = typer.Typer()


@idaq_cli.command()
def single(
    log_filepath: Path = typer.Option(None, exists=True, file_okay=True, dir_okay=False)
) -> None:
    """Process the provided log file."""
    if log_filepath is None:
        log_filepath = prompt_for_file()

    process_log_files([log_filepath])


@idaq_cli.command()
def batch(
    log_dir: Path = typer.Option(None, exists=True, file_okay=False, dir_okay=True),
    recurse: bool = False,
) -> None:
    """
    Batch process all logs in the provided directory.

    Recursive processing may be optionally specified (Default: False).
    """
    if log_dir is None:
        log_dir = prompt_for_dir()

    log_files = find_log_files(start_dir=log_dir, recurse=recurse)
    typer.echo(f"Found {len(log_files)} files to process")
    process_log_files(log_files)


@idaq_cli.callback(invoke_without_command=True, no_args_is_help=True)
def main(ctx: typer.Context) -> None:
    """Python Toolkit for the Wamore iDAQ."""
    # Provide a callback for the base invocation to display the help text & exit.
    pass


def process_log_files(log_files: t.List[Path]) -> None:
    """Execute log file processing pipeline for the provided log file(s)."""
    for log_file in log_files:
        typer.echo(f"(Fake) Processing: '{log_file}' ... ", nl=False)
        typer.echo(f"Done!")


if __name__ == "__main__":
    idaq_cli()
