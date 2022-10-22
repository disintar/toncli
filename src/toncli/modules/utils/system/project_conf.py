# Copyright (c) 2022 Disintar LLP Licensed under the Apache License Version 2.0

import os.path
import platform
import sys
from typing import List

import yaml
from colorama import Fore, Style

from toncli.modules.utils.system.log import logger

gr = Fore.GREEN
bl = Fore.CYAN
rs = Style.RESET_ALL


class TonProjectConfig:
    def __init__(self, func_files_locations: List[str], name: str, to_save_location: str, data: str, boc: str,
                 address: str, func_tests_files_locations: List[str], to_save_tests_location: str):
        self.name = name
        self.boc = boc
        self.address = address
        self.data = data
        self.to_save_location = to_save_location
        self.func_files_locations = func_files_locations
        self.func_tests_files_locations = func_tests_files_locations
        self.to_save_tests_location = to_save_tests_location

        if platform.system() == 'Windows':
            from toncli.modules.utils.system.conf import name_replace

            self.boc = boc.replace(name_replace[0], name_replace[1])
            self.address = address.replace(name_replace[0], name_replace[1])
            self.data = data.replace(name_replace[0], name_replace[1])
            self.to_save_location = to_save_location.replace(name_replace[0], name_replace[1])
            self.to_save_tests_location = to_save_tests_location.replace(name_replace[0], name_replace[1])
            self.func_files_locations = [i.replace(name_replace[0], name_replace[1]) for i in func_files_locations]
            self.func_tests_files_locations = [i.replace(name_replace[0], name_replace[1]) for i in
                                               func_tests_files_locations]

    def __repr__(self):
        return f"<TonProjectConfig {self.name}>"


class ProjectConf:
    def __init__(self, project_root: str):
        """Parse project.yaml to correctly build project"""
        self.contracts: List[TonProjectConfig] = []

        with open(os.path.abspath(f"{project_root}/project.yaml"), "r", encoding='utf-8') as stream:
            try:
                func_configuration = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logger.error(f"😒 Can't load {bl}project.yaml{rs} in {gr}{project_root}{rs}, error:")
                logger.error(exc)
                sys.exit()

        for contract in func_configuration:
            contract_config = func_configuration[contract]
            func_files_locations = [f"{project_root}/{file_path}" for file_path in contract_config['func']]

            if 'tests' in contract_config:
                func_tests_files_locations = [f"{project_root}/{file_path}" for file_path in contract_config['tests']]
            else:
                func_tests_files_locations = []

            self.contracts.append(TonProjectConfig(**{
                'func_files_locations': func_files_locations,
                'func_tests_files_locations': func_tests_files_locations,
                'name': contract,
                'boc': f"{project_root}/build/boc/{contract}.boc",
                'address': f"{project_root}/build/{contract}_address",
                'to_save_location': f"{project_root}/build/{contract}.fif",
                'to_save_tests_location': f"{project_root}/build/{contract}_tests.fif",
                'data': f"{project_root}/{contract_config['data']}" if 'data' in contract_config else ""
            }))
