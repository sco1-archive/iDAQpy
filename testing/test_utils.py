from pathlib import Path

import pytest
import pytest_check as check
from idaqpy import utils
from pytest_mock.plugin import MockFixture


@pytest.mark.skip(reason="Test generation in progress")
def test_log_file_discovery() -> None:
    """Check that supported log files are correctly parsed from a directory of candidate files."""
    raise NotImplementedError


def test_file_selection_ui(mocker: MockFixture) -> None:
    """Thin test for checking that the TkInter file selection dialog has been called."""
    # Mock tkinter so we can just check that the appropriate methods are called
    mocker.patch("tkinter.Tk")
    filedialog_patch = mocker.patch("tkinter.filedialog.askopenfilename")

    utils.prompt_for_file(Path())
    check.is_true(filedialog_patch.called)


def test_dir_selection_ui(mocker: MockFixture) -> None:
    """Thin test for checking that the TkInter directory selection dialog has been called."""
    # Mock tkinter so we can just check that the appropriate methods are called
    mocker.patch("tkinter.Tk")
    filedialog_patch = mocker.patch("tkinter.filedialog.askdirectory")

    utils.prompt_for_dir(Path())
    check.is_true(filedialog_patch.called)
