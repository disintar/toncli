import os
import shlex
import subprocess
import sys
from typing import Optional, List

from colorama import Fore, Style

from tncli.modules.utils.system.log import logger
from tncli.modules.utils.system.project import check_for_needed_files_to_deploy
from tncli.modules.utils.func.commands import build as fift_build
from tncli.modules.utils.system.conf import executable

bl = Fore.CYAN
rd = Fore.RED
gr = Fore.GREEN
rs = Style.RESET_ALL


class Func:
    def __init__(self, command: str, args: Optional[List[str]] = None, kwargs: Optional[dict] = None):
        self.command = command

        if kwargs:
            self.kwargs = kwargs
            self.kwargs['func_args'] = shlex.split(self.kwargs['func_args'])
        else:
            self.kwargs = {'func_args': []}

        self.args = args

        # Currently, running command in project root
        self.project_dir = check_for_needed_files_to_deploy(os.getcwd(), True)

    def run(self):
        if not self.command or self.command == 'build':
            self.build()
        elif self.command:
            command = [executable['func'], *self.kwargs['func_args'], self.command, *self.args, *self.kwargs]
            subprocess.run(command)
        else:
            logger.error("🔎 Can't find such command")
            sys.exit()

    def build(self):
        if not self.project_dir:
            logger.error(f"🤟 It is not project root [{bl}{os.getcwd()}{rs}] - I can't build project without project")
            sys.exit()

        # Build code
        fift_build(f"{os.getcwd()}/func/",
                   f"{os.getcwd()}/build/code.fif", cwd=os.getcwd())
        logger.info(f"🥌 Build [{bl}{os.getcwd()}{rs}] {gr}successfully{rs}, check out {gr}build/code.fif{rs}")
