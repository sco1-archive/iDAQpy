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


@pytest.mark.skip(reason="Test not implemented")
def test_single_file_entry(mocker: MockFixture) -> None:
    """Test UI flow for single file processing."""
    raise NotImplementedError


@pytest.mark.skip(reason="Test not implemented")
def test_batch_entry(mocker: MockFixture) -> None:
    """Test UI flow for batch file processing."""
    raise NotImplementedError
