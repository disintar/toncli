# Copyright (c) 2022 Disintar LLP Licensed under the Apache License Version 2.0

import os
import subprocess
import sys
import tempfile
from typing import List, Optional

from colorama import Fore, Style
from jinja2 import FileSystemLoader, select_autoescape, Environment

from toncli.modules.utils.system.conf import config_folder, executable, project_root, getcwd
from toncli.modules.utils.system.log import logger

bl = Fore.CYAN
rd = Fore.RED
gr = Fore.GREEN
rs = Style.RESET_ALL


# Run fift file with fift-libs folder
def fift_execute_command(file: str, args: List[str], pre_args: Optional[List[str]] = None) -> List[str]:
    if not pre_args:
        pre_args = []

    answer = [os.path.abspath(executable['fift']), "-I",
              os.path.abspath(f"{config_folder}/fift-libs"),
              *pre_args, "-s",
              os.path.abspath(file),
              *args]

    return answer


def test_fift(fift_files_locations: List[str], test_file_path: str, cwd: Optional[str] = None,
              data_params: Optional[list] = None):
    """
    :param fift_files_locations: files to pass to test.fif
    :param test_file_path: Path to test.fif file
    :param cwd: If you need to change root of running script pass it here
    :return:
    """
    logger.info(f"🤗 Run tests on {bl}{fift_files_locations}{rs}")

    if not data_params:
        data_params = [""]

    for file in fift_files_locations:
        # Run tests from fift and pass path to file
        # (example of tests can be found in toncli/modules/fift/run_test.fif)
        loader = FileSystemLoader(f"{project_root}/modules/fift")

        env = Environment(
            loader=loader,
            autoescape=select_autoescape()
        )

        template = env.get_template(test_file_path)

        run_test_temp_location: str = tempfile.mkstemp(suffix='.fif')[1]

        rendered = template.render(data_path=file)

        with open(run_test_temp_location, 'w', encoding='utf-8') as f:
            f.write(rendered)

        subprocess.run(fift_execute_command(run_test_temp_location, data_params), cwd=getcwd() if not cwd else cwd)


def contract_manipulation(code_path: str, data_path: str, workchain: int, boc_location: str, address_location: str,
                          cwd: Optional[str] = None, data_params: List[str] = None) -> Optional[str]:
    """Run contract_manipulation.fif code"""
    if not data_params:
        data_params = [""]

    logger.info(f"🥳 Start contract manipulation")

    # Load template of transaction_debug
    loader = FileSystemLoader(f"{project_root}/modules/fift")

    env = Environment(
        loader=loader,
        autoescape=select_autoescape()
    )

    template = env.get_template("data_proxy.fif.template")

    boc_temp_location: str = tempfile.mkstemp(suffix='.boc')[1]

    rendered = template.render(data_path=data_path, file_path=boc_temp_location)

    with open(boc_temp_location, 'w', encoding='utf-8') as f:
        f.write(rendered)

    command = fift_execute_command(boc_temp_location, data_params)
    output = subprocess.check_output(command, cwd=getcwd() if not cwd else cwd)
    output_data = output.decode()

    contract_manipulation_fift_path = os.path.join(project_root, "modules/fift/contract_manipulation.fif")
    command = fift_execute_command(contract_manipulation_fift_path,
                                   [code_path, boc_temp_location, str(workchain), boc_location, address_location])

    output = subprocess.check_output(command, cwd=getcwd() if not cwd else cwd)
    output_data = output.decode()

    # # TODO: fix, get normal address from python...
    if 'address' in output_data:
        return output_data
    else:
        logger.error(f"😳 {rd}Error{rs} on contract_manipulation, please double check everything.")
        logger.error(output_data)
        sys.exit()
