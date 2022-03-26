import os
import subprocess
import sys
from typing import Optional, List

import yaml
from colorama import Fore, Style

from toncli.modules.utils.system.conf import config_folder, executable
from toncli.modules.utils.system.log import logger
from toncli.modules.utils.system.project import migrate_project_struction
from toncli.modules.utils.system.project_conf import ProjectConf, TonProjectConfig

bl = Fore.CYAN
gr = Fore.GREEN
rs = Style.RESET_ALL


def build(project_root: str,
          cwd: Optional[str] = None,
          func_args: List[str] = None,
          contracts: List[TonProjectConfig] = None) -> Optional[str]:
    """
    Build func file(s) and save result fift file to location

    :param contracts: contracts to build
    :param func_args: add arguments to func
    :param project_root: Files to build in needed order
    :param cwd: If you need to change root of running script pass it here
    :return:
    """
    project_config = ProjectConf(project_root)

    if not contracts:
        contracts = project_config.contracts

    if not func_args:
        func_args = []

    output = []
    for contract in contracts:
        output.append(build_files(contract.func_files_locations, contract.to_save_location, func_args, cwd))

    return "\n".join(list(map(str, output)))


def build_files(func_files_locations: List[str], to_save_location: str, func_args: List[str] = None,
                cwd: Optional[str] = None):
    build_command = [os.path.abspath(executable['func']), *func_args, "-o",
                     os.path.abspath(to_save_location), "-SPA",
                     os.path.abspath(f"{config_folder}/func-libs/stdlib.func"), *func_files_locations]
    get_output = subprocess.check_output(build_command, cwd=os.getcwd() if not cwd else os.path.abspath(cwd))

    if get_output:
        return get_output.decode()
