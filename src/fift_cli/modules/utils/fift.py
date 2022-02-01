import os
import subprocess
from typing import List, Optional

from colorama import Fore, Style

from .conf import config_folder, executable
from .log import logger

bl = Fore.CYAN
gr = Fore.GREEN
rs = Style.RESET_ALL


# Run fift file with fift-libs folder
def fift_execute_command(file: str, args: List):
    return [executable['fift'], "-I", f"{config_folder}/fift-libs", "-s", file, *args]


def test_fift(fift_files_locations: List[str], test_file_path: str, cwd: Optional[str] = None):
    """
    :param fift_files_locations: files to pass to test.fif
    :param test_file_path: Path to test.fif file
    :param cwd: If you need to change root of running script pass it here
    :return:
    """
    logger.info(f"🤗 Run tests on {fift_files_locations}")

    for file in fift_files_locations:
        # Run tests from fift and pass path to file
        # (example of tests can be found in fift_cli/modules/fift/run_test.fif)
        subprocess.run(fift_execute_command(test_file_path, [file]), cwd=os.getcwd() if not cwd else cwd)
