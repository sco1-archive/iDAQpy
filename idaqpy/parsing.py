import subprocess
from pathlib import Path

import pandas as pd
from idaqpy import LogdecoderNotFound


def decode_raw_log(logdecoder_path: Path, data_filepath: Path) -> Path:
    """Decode raw binary log file to CSV using the provided external log decoder executable."""
    if not logdecoder_path.exists():
        raise LogdecoderNotFound(f"logdecoder could not be found. Expected at: '{logdecoder_path}'")

    # Pass log file to logdecoder, which will output a CSV to the same directory
    p = subprocess.run([logdecoder_path, data_filepath.absolute()])
    p.check_returncode()

    # If successful, replace the original log filepath with the decoded filepath
    return data_filepath.with_name(f"{data_filepath.name}.csv")


def parse_csv(csv_filepath: Path) -> pd.DataFrame:
    """Parse a decoded CSV log file into a DataFrame."""
    raise NotImplementedError
