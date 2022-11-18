# Copyright (c) 2022 Disintar LLP Licensed under the Apache License Version 2.0

import os
import platform
import shutil
import subprocess
from typing import Optional, List, Dict, Tuple, Union
from colorama import Fore, Style
from toncli.modules.utils.system.log import logger

bl = Fore.CYAN
gr = Fore.GREEN
rs = Style.RESET_ALL


def safe_get_version(executable: str, only_build_info: bool = True) -> Union[List[str], str]:
    try:
        output = subprocess.check_output([os.path.abspath(executable), '-V'])
        output = output.decode()

        if 'build information:' in output.lower():
            if only_build_info:
                output = output.split('[')[-1]
                output = output[:-1]
                return output.split(',')
            else:
                return output

    except Exception as e:
        logger.error(e)
        return ""


def check_executable(executable_config: Dict) -> Tuple[Dict, bool]:
    from toncli.modules.utils.system.conf import getcwd

    config = {}
    is_executable_changes = False

    for item in ['func', 'fift', 'lite-client']:
        if not executable_config[item] or len(executable_config[item]) == 0:
            founded_executable = False

            if platform.system() == 'Windows':
                item_name = f'{item}.exe'
            else:
                item_name = item

            if item_name in os.listdir(getcwd()):
                item_path = os.path.abspath(os.path.join(getcwd(), item_name))
                version_output = safe_get_version(item_path)

                if version_output is not None and len(version_output) == 2:
                    is_executable_changes = True
                    founded_executable = True
                    config[item] = item_path

                    logger.info(f"Adding path to executable {item} success!")

            while not founded_executable:
                logger.warning(f"🤖 Can't find executable for {item}, please specify it, e.g.: /usr/bin/{item}")
                config[item] = input("Path: ")

                version_output = safe_get_version(config[item])

                if version_output is not None and len(version_output) == 2:
                    logger.info(version_output)

                    # logger.info(f"""You should also update your binaries for this version. Please download the binaries depending on your system at the links provided. \n
                    # Windows : {bl}https://github.com/SpyCheese/ton/actions/runs/2618774052{rs} \n
                    # Linux : {bl}https://github.com/SpyCheese/ton/actions/runs/2585669126{rs} \n
                    # MacOs : {bl}https://github.com/SpyCheese/ton/actions/runs/2618664609{rs} \n""")

                    is_executable_changes = True
                    founded_executable = True
                else:
                    logger.warning("😅 Path is not correct, please double check it")

        elif not os.path.exists(os.path.abspath(executable_config[item])):
            executable_path = shutil.which(item)

            if executable_path:
                version_output = safe_get_version(executable_path)

                if len(version_output) == 2:
                    config[item] = executable_path

                    if config[item] != executable_config[item]:
                        is_executable_changes = True
                    continue
                else:
                    logger.error(f"😳 Executable path is not working correct, output: {version_output}")

            founded_executable = False

            while not founded_executable:
                logger.warning(f"🤖 Can't find executable for {item}, please specify it, e.g.: /usr/bin/{item}")
                config[item] = input("Path: ")

                version_output = safe_get_version(config[item])

                if version_output is not None and len(version_output) == 2:
                    is_executable_changes = True
                    founded_executable = True
                else:
                    logger.warning("😅 Path is not correct, please double check it")
        else:
            version_output = safe_get_version(executable_config[item])

            if version_output is not None and len(version_output) != 2:
                executable_config[item] = '/not-exising'
                return check_executable(executable_config)

            config[item] = executable_config[item]

    return config, is_executable_changes
