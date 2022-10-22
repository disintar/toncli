# Copyright (c) 2022 Disintar LLP Licensed under the Apache License Version 2.0

"""
Build file(s) and save result fift file to location
"""
import os
from subprocess import check_output
from typing import Optional, List

from colorama import Fore, Style

from toncli.modules.utils.system.conf import config_folder, executable, getcwd
from toncli.modules.utils.system.project_conf import ProjectConf, TonProjectConfig

bl = Fore.CYAN
gr = Fore.GREEN
rs = Style.RESET_ALL


def inclide_func_files(include_path: str) -> List[str]:
    init_path    = os.path.join(include_path, "__init__.func")
    include_list = []

    if os.path.isfile(init_path):
        include_list.append(init_path)
    else:
        for root, _, files in os.walk(include_path):
            for file in files:
                if file.endswith((".func", ".fc")):
                    include_list.append(os.path.join(root, file))

    return include_list

def build_test(project_root: str,
               cwd: Optional[str] = None,
               func_args: List[str] = None,
               contracts: List[TonProjectConfig] = None,
               compile_tests_with_contract: bool = True) -> Optional[str]:
    """
    build_test method params are :
        :param contracts: contracts to build
        :param func_args: add arguments to func
        :param project_root: Files to build in needed order
        :param cwd: If you need to change root of running script pass it here
        :param compile_tests_with_contract: If you want to be able to call contracts methods from tests, you need
        to compile them together
        :return:
    """
    if not contracts:
        project_config = ProjectConf(project_root)
        contracts = project_config.contracts

    if not func_args:
        func_args = []

    output = []
    func_and_test_files = []
    for contract in contracts:
        if len(contract.func_tests_files_locations):

            func_and_test_files.extend(inclide_func_files(f"{config_folder}/func-libs/"))
            func_and_test_files.extend(inclide_func_files(f"{config_folder}/test-libs/"))

            if compile_tests_with_contract:
                output.append(
                    build_test_files([*func_and_test_files, *contract.func_files_locations, *contract.func_tests_files_locations],
                                     contract.to_save_tests_location, [], cwd))
            else:
                output.append(
                    build_test_files(
                        contract.func_files_locations,
                        contract.to_save_tests_location, [], cwd))
                output.append(
                    build_test_files(
                        [*func_and_test_files, *contract.func_tests_files_locations],
                        contract.to_save_tests_location, [], cwd))

    return "\n".join(list(map(str, output)))


def build_test_files(func_files_locations: List[str],
                     to_save_location: str,
                     func_args: List[str] = None,
                     cwd: Optional[str] = None):
    """
    build_test_files method params are :
        :func_files_locations: location of the func files
        :param to_save_location: location to save the files
        :param func_args: add arguments to func
        :param cwd: If you need to change root of running script pass it here
        :return:
    """
    build_command = [os.path.abspath(executable['func']), *func_args, "-o",
                     os.path.abspath(to_save_location), "-SPA",
                     *[os.path.abspath(i) for i in func_files_locations]]

    get_output = check_output(build_command,
                              cwd=getcwd() if not cwd else os.path.abspath(cwd),
                              shell=False)

    if get_output:
        return get_output.decode()
