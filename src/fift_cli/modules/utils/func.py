import subprocess
from typing import List, Optional

from .conf import config_folder, executable


def build(func_files_location: List[str], to_save_location: str) -> Optional[str]:
    """
    Build func file(s) and save result fift file to location

    :param func_files_location: Files to build in needed order
    :param to_save_location: Location to save fift result
    :return:
    """

    build_command = [executable['func'], "-SPA",
                     f"{config_folder}/func-libs/stdlib.fc", *func_files_location,
                     "-o", to_save_location]

    get_output = subprocess.check_output(build_command)

    if get_output:
        return get_output.decode()
