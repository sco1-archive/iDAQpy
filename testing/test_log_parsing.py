import typing as t
from pathlib import Path

import pytest
from idaqpy import UnsupportedLogFile
from idaqpy.models import iDAQ
from pytest_mock.plugin import MockFixture


class UnsupportedFileTestCase(t.NamedTuple):
    """Represent unsupported file test cases & whether the file name should yield an error."""

    file_name: str
    should_raise: bool


UNSUPPORTED_FILE_CASES = (
    UnsupportedFileTestCase(file_name="file.exe", should_raise=True),
    UnsupportedFileTestCase(file_name="file.mat", should_raise=True),
    UnsupportedFileTestCase(file_name="LOG.001", should_raise=False),
    UnsupportedFileTestCase(file_name="file.idaq", should_raise=False),
    UnsupportedFileTestCase(file_name="file.csv", should_raise=False),
)


@pytest.mark.parametrize("file_name, should_raise", UNSUPPORTED_FILE_CASES)
def test_unsupported_raise(
    file_name: str, should_raise: bool, tmp_path: Path, mocker: MockFixture
) -> None:
    """
    Test that an error is appropriately raised for unsupported file types.

    A temporary directory is provided by Pytest as a fixture to create a dummy file to bypass
    log existence check.
    """
    # Create a temporary dummy file
    tempfile = tmp_path / file_name
    tempfile.write_text("")

    # Mock the data parsing methods since they're not relevant to this test
    mocker.patch("idaqpy.models.iDAQ.parse_raw_log")
    mocker.patch("idaqpy.models.iDAQ.parse_log_csv")

    if should_raise:
        with pytest.raises(UnsupportedLogFile):
            _ = iDAQ(tempfile)
    else:
        _ = iDAQ(tempfile)
