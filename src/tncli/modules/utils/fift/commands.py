import os
import subprocess
import sys
from typing import List, Optional

from colorama import Fore, Style

from tncli.modules.utils.system.conf import config_folder, executable, project_root
from tncli.modules.utils.system.log import logger

bl = Fore.CYAN
rd = Fore.RED
gr = Fore.GREEN
rs = Style.RESET_ALL


# Run fift file with fift-libs folder
def fift_execute_command(file: str, args: List[str], pre_args: Optional[List[str]] = None) -> List[str]:
    if not pre_args:
        pre_args = []

    return [executable['fift'], "-I", f"{config_folder}/fift-libs", *pre_args, "-s", file, *args]


def test_fift(fift_files_locations: List[str], test_file_path: str, cwd: Optional[str] = None):
    """
    :param fift_files_locations: files to pass to test.fif
    :param test_file_path: Path to test.fif file
    :param cwd: If you need to change root of running script pass it here
    :return:
    """
    logger.info(f"🤗 Run tests on {bl}{fift_files_locations}{rs}")

    for file in fift_files_locations:
        # Run tests from fift and pass path to file
        # (example of tests can be found in tncli/modules/fift/run_test.fif)
        subprocess.run(fift_execute_command(test_file_path, [file]), cwd=os.getcwd() if not cwd else cwd)


def contract_manipulation(code_path: str, data_path: str, workchain: int, boc_location: str, address_location: str,
                          cwd: Optional[str] = None) -> Optional[str]:
    """Run contract_manipulation.fif code"""

    logger.info(f"🥳 Start contract manipulation")

    contract_manipulation_fift_path = f"{project_root}/modules/fift/contract_manipulation.fif"
    command = fift_execute_command(contract_manipulation_fift_path,
                                   [code_path, data_path, str(workchain), boc_location, address_location])

    output = subprocess.check_output(command, cwd=os.getcwd() if not cwd else cwd)
    output_data = output.decode()

    # TODO: fix, get normal address from python...
    if 'address' in output_data:
        return output_data
    else:
        logger.error(f"😳 {rd}Error{rs} on contract_manipulation, please double check everything.")
        logger.error(output_data)
        sys.exit()
