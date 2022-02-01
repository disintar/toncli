import subprocess
from typing import List, Optional

import yaml
from colorama import Fore, Style

from .conf import config_folder, executable
from .log import logger

bl = Fore.CYAN
gr = Fore.GREEN
rs = Style.RESET_ALL


def build(func_folder_path: str, to_save_location: str) -> Optional[str]:
    """
    Build func file(s) and save result fift file to location

    :param func_files_locations: Files to build in needed order
    :param to_save_location: Location to save fift result
    :return:
    """

    with open(f"{func_folder_path}/files.yaml", "r") as stream:
        try:
            func_configuration = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.error(f"😒 Can't load {bl}files.yaml{rs} in {gr}{func_folder_path}{rs}, error:")
            logger.error(exc)
            return

    func_files_locations = [f"{func_folder_path}/{file}" for file in func_configuration['files']]

    build_command = [executable['func'], "-SPA",
                     f"{config_folder}/func-libs/stdlib.fc", *func_files_locations,
                     "-o", to_save_location]

    get_output = subprocess.check_output(build_command)

    if get_output:
        return get_output.decode()
