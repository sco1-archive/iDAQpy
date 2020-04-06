import typing as t
from pathlib import Path

import pytest
import pytest_check as check
from idaqpy.models import LogFileType, iDAQ


TEST_CASES = {
    LogFileType.RAW: (
        "LOG.001",
        "log.001",
        "Log.001",
        "LOG.1",
        "FILE.iDAQ",
        "file.idaq",
        "fIlE.IdAq",
        "LOG.001.iDAQ",
    ),
    LogFileType.DECODED: (
        "LOG.001.csv",
        "log.001_proc.csv",
        "FILE.001.csv",
        "TESTING.csv",
        "TESTING.CSV",
    ),
    LogFileType.MATLAB: ("LOG.001.mat", "LOG.001_proc.mat", "LOG.001.MAT", "FILE.mat", "file.mat",),
    LogFileType.UNSUPPORTED: ("LOG.001.JSON", "file.exe", "file.py", "FILE.py",),
}


@pytest.fixture(params=TEST_CASES.keys())
def build_test_case(request) -> t.Tuple[LogFileType, t.Tuple[str]]:  # noqa: ANN001
    """Create a fixture for the provided test cases."""
    log_type = request.param
    return log_type, TEST_CASES[log_type]


def test_log_classification(build_test_case: t.Tuple[LogFileType, t.Tuple[str]]) -> None:
    """Test for correct classification of log types."""
    log_type, file_names = build_test_case
    for file_name in file_names:
        failure_msg = f"Comparison failed for filename: '{file_name}'"
        check.equal(log_type, iDAQ.classify_log_type(Path(file_name)), msg=failure_msg)
