# Run fift file with fift-libs folder
import os
import subprocess
from typing import List, Optional, Tuple

from colorama import Fore, Style
from requests import get as http_get

from tncli.modules.utils.system.conf import executable, config_folder, config_uri
from tncli.modules.utils.system.log import logger

gr = Fore.GREEN
bl = Fore.CYAN
rs = Style.RESET_ALL


def get_network_config_path(network: str, update_config: bool = False) -> str:
    """
    Get network config locally or download it from config_uri

    :param network: Network to use
    :param update_config: Update cached config
    :return:
    """
    filename = f"{network}.json"

    # Find file and return path to it
    if filename not in os.listdir(config_folder) or update_config:
        logger.info(
            f"🏗  Config of {gr}{network}{rs} will be downloaded to {gr}{config_folder}{rs} "
            f"from {gr}{config_uri[network]}{rs}")

        # need to download config file and save it
        r = http_get(config_uri[network], stream=True)
        if r.status_code == 200:
            with open(f"{config_folder}/{filename}", 'wb') as f:
                for chunk in r:
                    f.write(chunk)

    return f"{config_folder}/{filename}"


def lite_client_execute_command(network: str, args: List[str], update_config=False, ) -> List[str]:
    """
    Execute command to lite_client

    :param network: network to use
    :param args: command args will pass to lite-client
    :param update_config: update cached config of nets or not
    :return:
    """
    network = get_network_config_path(network, update_config)
    return [executable['lite-client'], "-C", network, *args]


def get_account_status(network: str, address: str, cwd: Optional[str] = None,
                       update_config: bool = False) -> Tuple[float, bool]:
    """
    Get balance and inited / uninited status

    :param network: Account network
    :param address: Account address
    :param cwd: Optional path to run lite-client
    :return: balance, is_inited
    """
    command = lite_client_execute_command(network, ['-v', '0', '-c', f'getaccount {address}'],
                                          update_config=update_config)
    account_info = subprocess.check_output(command, cwd=os.getcwd() if not cwd else cwd)
    account_info = account_info.decode()
    is_inited = 'account_uninit' not in account_info

    account_info = account_info.split('\n')
    if account_info[-2] == 'account state is empty':
        return 0, False
    else:
        # TODO: not to use lite-client!
        return int(account_info[-2].split()[-1][:-2]) / 1000000000, is_inited


def send_boc(network: str, path: str, cwd: Optional[str] = None, update_config: bool = False,
             get_output: bool = False) -> Optional[str]:
    """
    Send BOC via lite-client

    :param get_output: Return output or not
    :param network: network to send
    :param path: path to boc file
    :param cwd: root dir run command from
    :param update_config: need to update local cached config of network
    :return:
    """
    command = lite_client_execute_command(network, ['-v', '2', '-c', f'sendfile {path}'], update_config=update_config)
    if not get_output:
        subprocess.run(command, cwd=os.getcwd() if not cwd else cwd)
    else:
        return subprocess.check_output(command, cwd=os.getcwd() if not cwd else cwd).decode()
