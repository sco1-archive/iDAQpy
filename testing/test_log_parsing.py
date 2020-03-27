import typing as t
from pathlib import Path

import pytest
from idaqpy import UnsupportedLogFile
from idaqpy.models import iDAQ


class UnsupportedFileTestCase(t.NamedTuple):
    """Represent unsupported file test cases & whether the filename should yield an error."""

    filepath: Path
    should_raise: bool


UNSUPPORTED_FILE_CASES = (
    UnsupportedFileTestCase(filepath=Path("file.exe"), should_raise=True),
    UnsupportedFileTestCase(filepath=Path("file.mat"), should_raise=True),
    UnsupportedFileTestCase(filepath=Path("LOG.001"), should_raise=False),
    UnsupportedFileTestCase(filepath=Path("file.idaq"), should_raise=False),
    UnsupportedFileTestCase(filepath=Path("file.csv"), should_raise=False),
)


@pytest.mark.parametrize("filepath, should_raise", UNSUPPORTED_FILE_CASES)
def test_unsupported_raise(filepath: Path, should_raise: bool) -> None:
    """Test that an error is appropriately raised for unsupported file types."""
    if should_raise:
        with pytest.raises(UnsupportedLogFile):
            _ = iDAQ(filepath)
    else:
        _ = iDAQ(filepath)
