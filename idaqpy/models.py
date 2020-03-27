from __future__ import annotations

from datetime import datetime
from enum import Enum, auto
from pathlib import Path

import pandas as pd
from idaqpy import UnsupportedLogFile


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
    log_name_patterns = {
        LogFileType.RAW: ("LOG.*", "*.iDAQ"),  # Will be passed to the log decoder executable
        LogFileType.DECODED: ("*.csv",),
        LogFileType.MATLAB: ("*.mat"),
    }

    def __init__(self, data_filepath: Path):
        self.data_filepath = data_filepath
        self.analysis_date = datetime.now()

        self.raw_data = self.parse_log_file(self.data_filepath)

    @classmethod
    def classify_log_type(cls, file_name: str) -> LogFileType:
        """Determine type of log file from its filename, as binned by `iDAQ.log_name_patterns`."""
        raise NotImplementedError

    @classmethod
    def parse_log_file(cls, filepath: Path) -> pd.DataFrame:
        """
        Parse the provided log file into a DataFrame.

        Parsing pipelines are determined by the file's name, as binned by `iDAQ.log_name_patterns`,
        raw log files are passed to Wamore's logdecoder executable to be converted into a CSV before
        being parsed into a DataFrame.
        """
        log_file_name = filepath.name
        log_type = cls.classify_log_type(log_file_name)
        if isinstance(log_type, LogFileType.UNSUPPORTED):
            raise UnsupportedLogFile(
                f"'{log_file_name}' does not match a supported file name pattern. "
                "A list of supported naming patterns is provided in the README."
            )

        if isinstance(log_type, LogFileType.MATLAB):
            raise UnsupportedLogFile("Support for MATLAB files is currently not implemented.")

        if isinstance(log_type, LogFileType.RAW):
            # TODO: Check for logdecoder
            # TODO: Pass log file to logdecoder & replace filepath with output file
            raise NotImplementedError

        # TODO: Parse CSV file
        raise NotImplementedError
