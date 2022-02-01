import subprocess
from typing import List

from colorama import Fore, Style

from .conf import config_folder, executable
from .log import logger

bl = Fore.CYAN
gr = Fore.GREEN
rs = Style.RESET_ALL


# Run fift file with fift-libs folder
def fift_execute_command(file: str, args: List):
    return [executable['fift'], "-I", f"{config_folder}/fift-libs", "-s", file, *args]


def test_fift(fift_files_locations: List[str], test_file_path: str):
    logger.info(f"🤗 Run tests on {fift_files_locations}")

    for file in fift_files_locations:
        # Run tests from fift and pass path to file
        # (example of tests can be found in fift_cli/modules/fift/run_test.fif)
        subprocess.run(fift_execute_command(test_file_path, [file]))
