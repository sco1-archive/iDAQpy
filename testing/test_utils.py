import typing as t
from pathlib import Path

import pytest
import pytest_check as check
from idaqpy import utils


class FileParsingTestCase(t.NamedTuple):
    """Helper container for log directory parsing test case generation."""

    log_filenames: t.Tuple[str]
    n_valid_logs: int


TEST_DIR_STRUCTURE = {
    "base": FileParsingTestCase(
        log_filenames=("LOG.001", "LOG.001.csv", "some_log.iDAQ", "LOG001.mat", "not_a.log",),
        n_valid_logs=4,
    ),
    "sub": FileParsingTestCase(log_filenames=("LOG.001", "LOG.002", "not_a.log",), n_valid_logs=2),
}


@pytest.fixture()
def log_dir(tmp_path_factory) -> Path:  # noqa: ANN001
    """
    Generate temporary directories of dummy log files to help test file discovery.

    The base temporary path is returned, which will contain all directories of test files.
    """
    base_dir = tmp_path_factory.mktemp("utils_test")
    for log_name in TEST_DIR_STRUCTURE["base"].log_filenames:
        log_file = base_dir / log_name
        log_file.write_text("")

    sub_dir = base_dir / "sub"
    sub_dir.mkdir()
    for log_name in TEST_DIR_STRUCTURE["sub"].log_filenames:
        log_file = sub_dir / log_name
        log_file.write_text("")

    return base_dir


def test_log_file_discovery(log_dir: Path) -> None:
    """
    Check that supported log files are correctly parsed from a directory of files.

    For simplicity, the check is currently limited to a comparison between the number of parsed log
    files and the provided truth value.
    """
    found_logs = utils.find_log_files(log_dir, recurse=False)
    check.equal(len(found_logs), TEST_DIR_STRUCTURE["base"].n_valid_logs)


def test_nested_log_file_discovery(log_dir: Path) -> None:
    """
    Check that supported log files are correctly parsed from a nested directory of files.

    For simplicity, the check is currently limited to a comparison between the number of parsed log
    files and the provided truth value.
    """
    found_logs = utils.find_log_files(log_dir, recurse=True)

    total_valid_logs = sum(test_case.n_valid_logs for test_case in TEST_DIR_STRUCTURE.values())
    check.equal(len(found_logs), total_valid_logs)
