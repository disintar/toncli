import os
import subprocess
import sys
from typing import Optional

import yaml
from colorama import Fore, Style

from .conf import config_folder, executable
from .log import logger

bl = Fore.CYAN
gr = Fore.GREEN
rs = Style.RESET_ALL


def build(func_folder_path: str, to_save_location: str, cwd: Optional[str] = None) -> Optional[str]:
    """
    Build func file(s) and save result fift file to location

    :param func_folder_path: Files to build in needed order
    :param to_save_location: Location to save fift result
    :param cwd: If you need to change root of running script pass it here
    :return:
    """

    with open(f"{func_folder_path}/files.yaml", "r") as stream:
        try:
            func_configuration = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.error(f"😒 Can't load {bl}files.yaml{rs} in {gr}{func_folder_path}{rs}, error:")
            logger.error(exc)
            sys.exit()

    func_files_locations = [f"{func_folder_path}/{file}" for file in func_configuration['files']]

    build_command = [executable['func'], "-SPA",
                     f"{config_folder}/func-libs/stdlib.fc", *func_files_locations,
                     "-o", to_save_location]

    get_output = subprocess.check_output(build_command, cwd=os.getcwd() if not cwd else cwd)

    if get_output:
        return get_output.decode()
