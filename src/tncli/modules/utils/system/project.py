import os
from colorama import Fore, Style

from tncli.modules.utils.system.log import logger
import sys

bl = Fore.CYAN
gr = Fore.GREEN
rs = Style.RESET_ALL


def check_for_needed_files_to_deploy(project_root: str, silence: bool = False) -> bool:
    """Check needed files and log if there is no one"""

    files = os.listdir(project_root)
    needed_structure = {
        'func': ['code.fc', 'files.yaml'],
        'fift': ['data.fif'],
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
