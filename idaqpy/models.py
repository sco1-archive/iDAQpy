from __future__ import annotations

import subprocess
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

    # Expand patterns for private use by utility functions
    _all_supported_patterns = []
    for patterns in log_name_patterns.values():
        _all_supported_patterns.extend(patterns)

    def __init__(self, data_filepath: Path, logdecoder_path_override: t.Optional[Path] = None):
        self.data_filepath = data_filepath
        self._logdecoder_path_override = logdecoder_path_override

        self.analysis_date = datetime.now()
        self.raw_data = self.parse_log_file()

    @property
    def logdecoder_path(self) -> Path:
        """Provide OS-specific path to logdecoder executable, or the overridden path if present."""
        if self._logdecoder_path_override:
            return self._logdecoder_path_override

        # Set up default path to the logdecoder executable. If on Windows we'll need `*.exe`
        logdecoder_base_path = Path("./logdecoder/")
        platform = sys.platform
        if platform in ("win32", "cygwin"):
            return logdecoder_base_path / "logdecoder.exe"
        else:
            return logdecoder_base_path / "logdecoder"

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
            self.data_filepath = self.parse_raw_log(self.logdecoder_path, self.data_filepath)

        # If we've gotten here, have a CSV to parse
        self.parse_log_csv()

    def parse_log_csv(self) -> None:
        """Parse a decoded CSV log file into a DataFrame."""
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

    @staticmethod
    def parse_raw_log(logdecoder_path: Path, data_filepath: Path) -> Path:
        """Decode raw binary log file to CSV using the provided external log decoder executable."""
        if not logdecoder_path.exists():
            raise LogdecoderNotFound(
                f"logdecoder could not be found. Expected at: '{logdecoder_path}'"
            )

        # Pass log file to logdecoder, which will output a CSV to the same directory
        p = subprocess.run([logdecoder_path, data_filepath.absolute()])
        p.check_returncode()

        # If successful, replace the original log filepath with the decoded filepath
        return data_filepath.with_name(f"{data_filepath.name}.csv")
