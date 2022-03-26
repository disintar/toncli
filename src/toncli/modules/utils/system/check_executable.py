import os
import shutil
import subprocess
from typing import Optional, List, Dict, Tuple
from toncli.modules.utils.system.log import logger


def safe_get_version(executable: str) -> Optional[List[str]]:
    try:
        output = subprocess.check_output([os.path.abspath(executable), '-V'])
        output = output.decode()

        if ' build information:' in output:
            output = output.split('[')[-1]
            output = output[:-1]
            return output.split(',')
    except Exception as e:
        logger.error(e)
        return


def check_executable(executable_config: Dict) -> Tuple[Dict, bool]:
    config = {}
    is_executable_changes = False

    for item in ['func', 'fift', 'lite-client']:
        if not os.path.exists(os.path.abspath(executable_config[item])):
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
