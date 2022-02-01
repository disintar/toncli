# Run fift file with fift-libs folder
import os
import subprocess
from typing import List, Optional, Tuple

from .conf import executable, config_folder


def lite_client_execute_command(network: str, args: List):
    return [executable['lite-client'], "-C", f"{config_folder}/{network}.json", *args]


def get_account_status(network: str, address: str, cwd: Optional[str] = None) -> Tuple[float, bool]:
    """
    Get balance and inited / uninited status

    :param network: Account network
    :param address: Account address
    :param cwd: Optional path to run lite-client
    :return: balance, is_inited
    """
    command = lite_client_execute_command(network, ['-v', '0', '-c', f'getaccount {address}'])
    account_info = subprocess.check_output(command, cwd=os.getcwd() if not cwd else cwd)
    account_info = account_info.decode()
    is_inited = 'account_uninit' not in account_info

    account_info = account_info.split('\n')
    if account_info[-2] == 'account state is empty':
        return 0, is_inited
    else:
        # TODO: not to use lite-client!
        return int(account_info[-2].split()[-1][:-2]) / 1000000000, is_inited


def send_boc(network: str, path: str, cwd: Optional[str] = None):
    command = lite_client_execute_command(network, ['-v', '0', '-c', f'sendfile {path}'])
    subprocess.run(command, cwd=os.getcwd() if not cwd else cwd)
