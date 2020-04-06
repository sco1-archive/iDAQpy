from pathlib import Path

import typer


idaq_cli = typer.Typer()


@idaq_cli.command()
def single(log_filepath: Path = typer.Option(None)) -> None:
    """Process the provided log file."""
    if log_filepath is None:
        print(f"No path provided, prompt the user to select")
        return

    print(f"Log path: {log_filepath}")


@idaq_cli.command()
def batch(log_dir: Path = typer.Option(None), recurse: bool = False) -> None:
    """
    Batch process all logs in the provided directory.

    Recursive processing may be optionally specified (Default: False).
    """
    if log_dir is None:
        print(f"No path provided, prompt the user to select")
        return

    print(f"Log directory: {log_dir}, Recurse: {recurse}")


@idaq_cli.callback(invoke_without_command=True, no_args_is_help=True)
def main(ctx: typer.Context) -> None:
    """Python Toolkit for the Wamore iDAQ."""
    # Provide a callback for the base invocation to display the help text & exit.
    pass


if __name__ == "__main__":
    idaq_cli()
