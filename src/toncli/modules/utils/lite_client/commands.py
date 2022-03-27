# Run fift file with fift-libs folder
import os
import subprocess
from typing import List, Optional, Tuple

from colorama import Fore, Style
from requests import get as http_get

from toncli.modules.utils.system.conf import executable, config_folder, config_uri, getcwd
from toncli.modules.utils.system.log import logger
from toncli.modules.utils.system.conf import lite_client_tries

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
            with open(os.path.abspath(f"{config_folder}/{filename}"), 'wb') as f:
                for chunk in r:
                    f.write(chunk)

    return os.path.abspath(f"{config_folder}/{filename}")


def lite_client_execute_command(network: str, args: List[str], update_config=False, ) -> List[str]:
    """
    Execute command to lite_client

    :param network: network to use
    :param args: command args will pass to lite-client
    :param update_config: update cached config of nets or not
    :return:
    """
    network = get_network_config_path(network, update_config)
    return [os.path.abspath(executable['lite-client']), "-v", "3", "--timeout", "3", "-C", network, *args]


def get_account_status(network: str, address: str, cwd: Optional[str] = None,
                       update_config: bool = False, block_id_ext: str = None) -> Tuple[float, bool]:
    """
    Get balance and inited / uninited status

    :param block_id_ext: Block to get status from
    :param update_config: Update config
    :param network: Account network
    :param address: Account address
    :param cwd: Optional path to run lite-client
    :return: balance, is_inited
    """
    command = lite_client_execute_command(network, ['-v', '0', '-c',
                                                    f'getaccount {address} {block_id_ext if block_id_ext else ""}'],
                                          update_config=update_config)

    _try = 0
    e = None
    while _try < lite_client_tries + 1:
        try:
            account_info = subprocess.check_output(command, cwd=getcwd() if not cwd else os.path.abspath(cwd))
            account_info = account_info.decode()
            break
        except Exception as exc:
            _try += 1
            e = exc

    if _try == lite_client_tries + 1:
        logger.error(f"😢 Error running {' '.join(command)}")
        raise e

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
        _try = 0
        e = None
        while _try < lite_client_tries + 1:
            try:
                subprocess.run(command, cwd=getcwd() if not cwd else os.path.abspath(cwd))
                break
            except Exception as exc:
                e = exc
                _try += 1

        if _try == lite_client_tries + 1:
            logger.error(f"😢 Error running {' '.join(command)}")
            raise e
    else:
        _try = 0
        e = None
        while _try < lite_client_tries + 1:
            try:
                output = subprocess.check_output(command, cwd=getcwd() if not cwd else os.path.abspath(cwd)).decode()
                break
            except Exception as exc:
                e = exc
                _try += 1

        if _try == lite_client_tries + 1:
            logger.error(f"😢 Error running {' '.join(command)}")
            raise exc
        return output


if __name__ == "__main__":
    print(get_account_status('testnet', 'kQDmJ8fyL7VWitcVXv1-CL4iu-xo5mXlSMZCXuIPxyy9yAHG'))
