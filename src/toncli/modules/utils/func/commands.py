# Copyright (c) 2022 Disintar LLP Licensed under the Apache License Version 2.0

"""
Build func file(s) and save result fift file to location
"""
import os
from subprocess import check_output
from typing import Optional, List

from colorama import Fore, Style

from toncli.modules.utils.system.check_executable import safe_get_version
from toncli.modules.utils.system.conf import config_folder, executable, getcwd, project_root
from toncli.modules.utils.system.project_conf import ProjectConf, TonProjectConfig

bl = Fore.CYAN
gr = Fore.GREEN
rs = Style.RESET_ALL


def build(ton_project_root: str,
          cwd: Optional[str] = None,
          func_args: List[str] = None,
          contracts: List[TonProjectConfig] = None) -> Optional[str]:
    """
    build method params are :
        :param contracts: contracts to build
        :param func_args: add arguments to func
        :param ton_project_root: Files to build in needed order
        :param cwd: If you need to change root of running script pass it here
        :return:
    """
    if not contracts:
        project_config = ProjectConf(ton_project_root)
        contracts = project_config.contracts

    if not func_args:
        func_args = []

    output = []

    fift_version = safe_get_version(executable['fift'], False).replace(os.linesep, " ")
    func_version = safe_get_version(executable['func'], False).replace(os.linesep, " ")

    for contract in contracts:
        output.append(
            build_files(contract.func_files_locations, contract.to_save_location, func_args, cwd))

        real_cwd = getcwd() if not cwd else os.path.abspath(cwd)

        save_boc_and_json_path = os.path.abspath(os.path.join(project_root, "modules/fift/save_boc_and_base64.fif"))
        save_boc_and_json = [os.path.abspath(executable['fift']), "-I", os.path.abspath(f"{config_folder}/fift-libs"),
                             "-s", save_boc_and_json_path, os.path.join(real_cwd, "build"), contract.name, fift_version,
                             func_version, contract.name]

        check_output(save_boc_and_json, cwd=real_cwd, shell=False)

    return "\n".join(list(map(str, output)))


def build_files(func_files_locations: List[str], to_save_location: str, func_args: List[str] = None,
                cwd: Optional[str] = None):
    """
    build_files method params are :
        :func_files_locations: location of the func files
        :param to_save_location: location to save the files
        :param func_args: add arguments to func
        :param cwd: If you need to change root of running script pass it here
        :return:
    """
    func_files = []
    for root, _, files in os.walk(f"{config_folder}/func-libs/"):
        for file in files:
            if file.endswith((".func", ".fc")):
                func_files.append(os.path.join(root, file))

    build_command = [os.path.abspath(executable['func']), *func_args, "-o",
                     os.path.abspath(to_save_location), "-SPA",
                     *[os.path.abspath(i) for i in func_files],
                     *[os.path.abspath(i) for i in func_files_locations]]
    get_output = check_output(build_command,
                              cwd=getcwd() if not cwd else os.path.abspath(cwd),
                              shell=False)

    if get_output:
        return get_output.decode()
