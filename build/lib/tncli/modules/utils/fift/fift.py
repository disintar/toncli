import os
import shlex
import subprocess
import sys
import tempfile
from typing import List, Optional

from colorama import Fore, Style

from tncli.modules.utils.func.func import Func
from tncli.modules.utils.system.conf import config_folder, executable
from tncli.modules.utils.fift.commands import fift_execute_command
from tncli.modules.utils.lite_client.commands import lite_client_execute_command
from tncli.modules.utils.system.log import logger
from tncli.modules.utils.system.project import check_for_needed_files_to_deploy

bl = Fore.CYAN
rd = Fore.RED
gr = Fore.GREEN
rs = Style.RESET_ALL


class Fift:
    def __init__(self, command: str, args: Optional[List[str]] = None, kwargs: Optional[dict] = None,
                 quiet: Optional[bool] = False, cwd: Optional[str] = None):
        """
        Easy interact with fift command

        :param command: command to run
        :param args: argumets passed to command
        :param kwargs: kwargs
        :param quiet: Is output of lite-client needed
        :param cwd: Project root
        """
        self.cwd = cwd if cwd else os.getcwd()
        self.command = command
        self.quiet = quiet

        if kwargs:
            self.kwargs = kwargs
            self.kwargs['fift_args'] = shlex.split(self.kwargs['fift_args'])
            self.kwargs['lite_client_args'] = shlex.split(self.kwargs['lite_client_args'])
        else:
            self.kwargs = {'fift_args': [],
                           'lite_client_args': [],
                           'build': False,
                           'net': 'testnet',
                           'update': False}

        self.args = args

        # Currently, running command in project root
        self.project_dir = check_for_needed_files_to_deploy(os.getcwd(), True)
        self.cli_fif_lib = None

    def run(self):
        """Run specific command"""

        if not self.command or self.command == 'interactive':
            self.run_interactive()
        elif self.command == 'run':
            self.run_script()
        elif self.command == 'sendboc':
            return self.sendboc()
        else:
            logger.error("🔎 Can't find such command")
            sys.exit()

    def sendboc(self):
        """Send BOC to blockchain"""
        from tncli.modules.utils.fift.cli_lib import build_cli_lib

        if not len(self.args):
            logger.error("👉 You need to specify FIFT file path to sendboc")
            sys.exit()

        filename = self.args[0]

        # Check that
        with open(filename, 'r') as f:
            code = f.read()

            if 'saveboc' not in code:
                logger.error(f"🦷 You need to add {bl}saveboc{rs} to your fif file {gr}{filename}{rs}")
                sys.exit()

        # remove folder
        if '/' in filename:
            filename = filename.split('/')[-1]

        # get file-base
        if '.' in filename:
            filename = filename.split('.')[0]

        if os.path.exists(f'{self.cwd}/build/boc'):
            path = f'{self.cwd}/build/boc/{filename}.boc'
        else:
            # if not project root - create temp directory
            path = tempfile.mkdtemp()
            path = f"{path}/{filename}.boc"

        logger.info(f"💾 Will save BOC to {gr}{path}{rs}")

        # If we never created cli.fif in project root
        if self.project_dir:
            self.cli_fif_lib = build_cli_lib(f'{self.cwd}/build/cli.fif', {  # Generate cli.fif
                "is_project": '1',
                "project_root": self.cwd,
                "build_path": path,
            })

        # If it's not project root
        elif not self.project_dir:
            self.cli_fif_lib = build_cli_lib(render_kwargs={
                "is_project": '0',
                "project_root": f'/tmp',
                "build_path": path
            })

        # generate BOC file
        # Our own cli.fif file need to be added before run
        command = fift_execute_command(file=self.args[0], args=[*self.args[1:]], pre_args=["-L", self.cli_fif_lib])

        subprocess.run(command, cwd=self.cwd)

        # send boc file
        command = lite_client_execute_command(self.kwargs['net'], ['-v', '2', '-c', f'sendfile {path}'],
                                              update_config=self.kwargs['update'])
        output = None
        if self.quiet:
            output = open(os.devnull, 'w')
        subprocess.run(command, stdout=output, stderr=output, cwd=self.cwd)

    def run_script(self):
        """Runs fift in script mode on file"""
        if not len(self.args):
            logger.error("👉 You need to specify file path to run")
            sys.exit()

        if not len(self.kwargs['fift_args']):
            self.kwargs['fift_args'] = ["-I", f"{config_folder}/fift-libs", "-s"]
        else:
            self.kwargs['fift_args'].append("-s")

        if self.project_dir and self.kwargs['build']:
            func = Func()
            func.run()

        command = [executable['fift'], *self.kwargs['fift_args'], *self.args]

        subprocess.run(command)

    def run_interactive(self):
        """Run interactive fift"""
        logger.info(f"🖥  Run interactive fift for you ({bl}Ctrl+c{rs} to exit)")
        logger.info(f"🖥  A simple Fift interpreter. Type `bye` to quit, or `words` to get a list of all commands")
        if not len(self.kwargs['fift_args']):
            self.kwargs['fift_args'] = ["-I", f"{config_folder}/fift-libs", "-i"]
        else:
            self.kwargs['fift_args'].append("-i")

        command = [executable['fift'], *self.kwargs['fift_args']]
        logger.debug(f"🖥  Command ({command})")

        try:
            subprocess.run(command)
        except KeyboardInterrupt:
            logger.info("🖥  Bye! Have a good code!)")
            sys.exit()
