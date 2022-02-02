import os
import shlex
import subprocess
import sys
import tempfile
from typing import List, Optional

from colorama import Fore, Style

from tncli.modules.utils.conf import config_folder, executable, project_root
from tncli.modules.utils.log import logger

bl = Fore.CYAN
rd = Fore.RED
gr = Fore.GREEN
rs = Style.RESET_ALL


# Run fift file with fift-libs folder
def fift_execute_command(file: str, args: List):
    return [executable['fift'], "-I", f"{config_folder}/fift-libs", "-s", file, *args]


def test_fift(fift_files_locations: List[str], test_file_path: str, cwd: Optional[str] = None):
    """
    :param fift_files_locations: files to pass to test.fif
    :param test_file_path: Path to test.fif file
    :param cwd: If you need to change root of running script pass it here
    :return:
    """
    logger.info(f"🤗 Run tests on {bl}{fift_files_locations}{rs}")

    for file in fift_files_locations:
        # Run tests from fift and pass path to file
        # (example of tests can be found in tncli/modules/fift/run_test.fif)
        subprocess.run(fift_execute_command(test_file_path, [file]), cwd=os.getcwd() if not cwd else cwd)


def contract_manipulation(code_path: str, data_path: str, workchain: int, cwd: Optional[str] = None) -> Optional[str]:
    logger.info(f"🥳 Start contract manipulation")

    contract_manipulation_fift_path = f"{project_root}/fift_cli/modules/fift/contract_manipulation.fif"
    command = fift_execute_command(contract_manipulation_fift_path, [code_path, data_path, str(workchain)])

    output = subprocess.check_output(command, cwd=os.getcwd() if not cwd else cwd)
    output_data = output.decode()

    # TODO: fix, get normal address from python...
    if 'address' in output_data:
        return output_data
    else:
        logger.error(f"😳 {rd}Error{rs} on contract_manipulation, please double check everything.")
        logger.error(output_data)
        sys.exit()


class Fift:
    def __init__(self, command: str, args: List[str], kwargs: dict):
        self.command = command

        self.kwargs = kwargs
        self.kwargs['fift_args'] = shlex.split(self.kwargs['fift_args'])
        self.kwargs['lite_client_args'] = shlex.split(self.kwargs['lite_client_args'])

        self.args = args

    def run(self):
        if not self.command or self.command == 'interactive':
            self.run_interactive()
        elif self.command == 'run':
            self.run_script()
        elif self.command == 'sendboc':
            self.sendboc()
        else:
            logger.error("🔎 Can't find such command")

    def sendboc(self):
        """Send BOC to blockchain"""
        if not len(self.args):
            logger.error("👉 You need to specify FIFT file path to sendboc")
            sys.exit()

        filename = self.args[0]

        # remove folder
        if '/' in filename:
            filename = filename.split('/')[-1]

        # get file-base
        if '.' in filename:
            filename = filename.split('.')[0]

        # if not project root - create temp directory
        path = tempfile.mkdtemp()
        if os.path.exists(f'{os.getcwd()}/build/boc'):
            path = f'{os.getcwd()}/build/boc/{filename}.boc'
        else:
            path = f"{path}/{filename}.boc"

        logger.info(f"💾 Will save BOC to {gr}{path}{rs}")

        # generate BOC file
        command = fift_execute_command(f"{project_root}/fift_cli/modules/fift/sendboc.fif", [self.args[0], path])
        subprocess.run(command)

    def run_script(self):
        """Runs fift in script mode on file"""
        if not len(self.args):
            logger.error("👉 You need to specify file path to run")
            sys.exit()

        if not len(self.kwargs['fift_args']):
            self.kwargs['fift_args'] = ["-I", f"{config_folder}/fift-libs", "-s"]
        else:
            self.kwargs['fift_args'].append("-s")

        command = [executable['fift'], *self.kwargs['fift_args'], *self.args]

        subprocess.run(command)

    def run_interactive(self):
        """Run interactive fift"""
        logger.info(f"🖥  Run interactive fift for you ({bl}Ctrl+c{rs} to exit)")
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
