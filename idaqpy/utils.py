import tkinter as tk
from pathlib import Path
from tkinter import filedialog


def prompt_for_file(start_dir: Path = Path()) -> Path:
    """Open a Tk file selection dialog to prompt the user to select a single file for processing."""
    root = tk.Tk()
    root.withdraw()

    # TODO: Add extension filter based on the iDAQ class parameters
    return Path(
        filedialog.askopenfilename(
            title="Select log file for processing.", initialdir=start_dir, multiple=False,
        )
    )


def prompt_for_dir(start_dir: Path = Path()) -> Path:
    """Open a Tk file selection dialog to prompt the user to select a directory for processing."""
    root = tk.Tk()
    root.withdraw()

    return Path(
        filedialog.askdirectory(
            title="Select log directory for batch processing.", initialdir=start_dir,
        )
    )
