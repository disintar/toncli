# Copyright (c) 2022 Disintar LLP Licensed under the Apache License Version 2.0

import os
import shutil

from colorama import Fore, Style

from toncli.modules.utils.system.log import logger
import sys
import yaml

bl = Fore.CYAN
gr = Fore.GREEN
rs = Style.RESET_ALL


def check_for_needed_files_to_deploy(project_root: str, silence: bool = False) -> bool:
    """Check needed files and log if there is no one"""

    files = os.listdir(project_root)
    needed_structure = {
        'func': [],
        'fift': [],
        'build': ['boc']
    }

    for folder in needed_structure:
        if folder not in files:
            if not silence:
                logger.error(f"🚫 It is not project root, there is no folder {bl}{folder}{rs} - I can't deploy it")
                sys.exit()
            else:
                return False

        for file in needed_structure[folder]:
            folder_files = os.listdir(f"{project_root}/{folder}")

            if file not in folder_files:
                if not silence:
                    logger.error(
                        f"🚫 It is not project root, there is no file {bl}{file}{rs} folder {bl}{folder}{rs} "
                        f"- I can't deploy it")
                    sys.exit()
                else:
                    return False
    return True


def migrate_project_struction(old_version: str, cwd: str):
    """
    Project struction migration

    :param cwd: project root
    :param old_version: Version to migrate from
    :return:
    """

    if old_version == '0.0.14':
        logger.warning("🙀 Detected old version of project, migrate to newer one")

        func_files_path = f"{cwd}/func/files.yaml"
        with open(f"{func_files_path}", "r", encoding='utf-8') as stream:
            try:
                func_configuration = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                logger.error(f"😒 Can't load {bl}files.yaml{rs} in {gr}{func_files_path}{rs}, error:")
                logger.error(exc)
                sys.exit()

        new_structure = {
            'contract': {
                'func': [f"func/{file}" for file in func_configuration['files']],
                'data': 'fift/data.fif'
            }
        }

        yaml_structure = yaml.dump(new_structure)

        with open(os.path.abspath(f"{cwd}/project.yaml"), "w", encoding='utf-8') as stream:
            stream.write(yaml_structure)

        if os.path.exists(os.path.abspath(f'{cwd}/build/address_text')):
            shutil.move(os.path.abspath(f"{cwd}/build/address_text"),
                        os.path.abspath(f"{cwd}/build/contract_address"))

        os.remove(func_files_path)
        logger.info("☀ Successful migrated to v0.0.15 project structure")
