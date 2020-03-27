from __future__ import annotations

import sys
import typing as t
from datetime import datetime
from enum import Enum, auto
from fnmatch import fnmatch
from pathlib import Path

import pandas as pd
from idaqpy import LogdecoderNotFound, UnsupportedLogFile


class LogFileType(Enum):
    """Represent the supported log file types."""

    DECODED = auto()
    MATLAB = auto()
    RAW = auto()
    UNSUPPORTED = auto()


class iDAQ:  # noqa: N801
    """Data model for the iDAQ log file."""

    # Bin supported file extensions to determine parsing behavior
    # NOTE: Downstream processing is case-insensitive
    # NOTE: Raw log files matching the "LOG.*" pattern are assumed to follow LOG.001, LOG.002, etc.
    log_name_patterns = {
        LogFileType.RAW: ("LOG.*", "*.iDAQ"),  # Will be passed to the log decoder executable
        LogFileType.DECODED: ("*.csv",),
        LogFileType.MATLAB: ("*.mat",),
    }

    # Set up default path to the logdecoder executable. If on windows we'll need `*.exe`
    logdecoder_base_path = Path("./logdecoder/")
    if sys.platform == "win32":
        logdecoder_path = logdecoder_base_path / "logdecoder.exe"
    else:
        logdecoder_path = logdecoder_base_path / "logdecoder"

    def __init__(self, data_filepath: Path, logdecoder_path_override: t.Optional[Path] = None):
        self.data_filepath = data_filepath
        self.analysis_date = datetime.now()

        if logdecoder_path_override:
            self.logdecoder_path = logdecoder_path_override

        self.raw_data = self.parse_log_file()

    def check_for_logdecoder(self) -> bool:
        """Check that the logdecoder executable is available in the configured location."""
        return self.logdecoder_path.exists()

    def parse_log_file(self) -> pd.DataFrame:
        """
        Parse the instance's log file into a DataFrame.

        Parsing pipelines are determined by the file's name, as binned by `iDAQ.log_name_patterns`,
        raw log files are passed to Wamore's logdecoder executable to be converted into a CSV before
        being parsed into a DataFrame.
        """
        if not self.data_filepath.exists():
            raise ValueError(f"Log file could not be found: '{self.data_filepath}'")

        log_type = self.classify_log_type(self.data_filepath)
        if log_type == LogFileType.UNSUPPORTED:
            raise UnsupportedLogFile(
                f"'{self.data_filepath.name}' does not match a supported file name pattern. "
                "A list of supported naming patterns is provided in the README."
            )

        if log_type == LogFileType.MATLAB:
            raise UnsupportedLogFile("Support for MATLAB files is currently not implemented.")

        if log_type == LogFileType.RAW:
            if not self.check_for_logdecoder():
                raise LogdecoderNotFound(
                    f"logdecoder could not be found. Expected at: '{self.logdecoder_path}'"
                )

            # TODO: Pass log file to logdecoder & replace filepath with output file
            raise NotImplementedError

        # TODO: Parse CSV file
        raise NotImplementedError

    @classmethod
    def classify_log_type(cls, filepath: Path) -> LogFileType:
        """
        Determine type of log file from its filename, as binned by `iDAQ.log_name_patterns`.

        NOTE: Comparison is case-insensitive
        """
        file_name = filepath.name.lower()
        for log_type, patterns in cls.log_name_patterns.items():
            for pattern in patterns:
                if fnmatch(file_name, pattern.lower()):
                    if pattern == "LOG.*":
                        # Because the default iDAQ log name is LOG.nnn, and the default decoder
                        # behavior is to append ".csv", we need to special case the raw file
                        # detection to also check for the all-numeric file extension
                        if not filepath.suffix[1:].isnumeric():
                            continue
                        else:
                            return log_type

                    return log_type
        else:
            return LogFileType.UNSUPPORTED
