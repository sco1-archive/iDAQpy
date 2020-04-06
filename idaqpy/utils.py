import tkinter as tk
import typing as t
from pathlib import Path
from tkinter import filedialog

from idaqpy.models import iDAQ


SUPPORTED_LOG_PATTERNS = iDAQ._all_supported_patterns


def prompt_for_file(start_dir: Path = Path()) -> Path:
    """Open a Tk file selection dialog to prompt the user to select a single file for processing."""
    root = tk.Tk()
    root.withdraw()

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


def find_log_files(start_dir: Path, recurse: bool) -> t.Set[Path]:
    """
    Locate supported log files for processing in the provided directory.

    Recursive processing may be optionally specified.

    NOTE: Case sensitivity is OS-specific
    """
    log_files = set()
    for pattern in SUPPORTED_LOG_PATTERNS:
        if recurse:
            pattern = f"**/{pattern}"

        log_files.update(start_dir.glob(pattern))

    return log_files
