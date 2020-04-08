import pytest
import pytest_check as check
from idaqpy.interface import idaq_cli
from pytest_mock.plugin import MockFixture
from typer.testing import CliRunner


RUNNER = CliRunner()


@check.check_func
def is_help(stdout_str: str) -> None:
    """
    Check that the provided string is a Typer help output.

    This check is accomplished by searching for the presence of all of the specified keywords
    """
    keywords = ("Usage", "Options", "Commands")

    assert all(keyword in stdout_str for keyword in keywords)


def test_base_invokes_help() -> None:
    """Check that the help invocation callback is properly invoked on a bare call of the CLI."""
    result = RUNNER.invoke(idaq_cli)
    is_help(result.stdout)


def test_single_file_ui_prompt(mocker: MockFixture) -> None:
    """Test that a bare invocation of the single file processing prompts user for file selection."""
    # Mock TkInter & processing flow so we can just check that the appropriate methods are called
    mocker.patch("tkinter.Tk")
    filedialog_patch = mocker.patch("tkinter.filedialog.askopenfilename")
    mocker.patch("idaqpy.interface.process_log_files")

    result = RUNNER.invoke(idaq_cli, ["single"])
    check.equal(result.exit_code, 0)
    check.is_true(filedialog_patch.called)


def test_batch_ui_prompt(mocker: MockFixture) -> None:
    """Test that a bare invocation of the batch processing prompts user for directory selection."""
    # Mock TkInter & processing flow so we can just check that the appropriate methods are called
    mocker.patch("tkinter.Tk")
    filedialog_patch = mocker.patch("tkinter.filedialog.askdirectory")
    mocker.patch("idaqpy.interface.process_log_files")

    result = RUNNER.invoke(idaq_cli, ["batch"])
    check.equal(result.exit_code, 0)
    check.is_true(filedialog_patch.called)


@pytest.mark.skip(reason="Test not implemented")
def test_single_file_entry(mocker: MockFixture) -> None:
    """Test UI flow for single file processing."""
    raise NotImplementedError


@pytest.mark.skip(reason="Test not implemented")
def test_batch_entry(mocker: MockFixture) -> None:
    """Test UI flow for batch file processing."""
    raise NotImplementedError
