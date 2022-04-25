from toncli.modules.utils.system.log import logger
import os
from appdirs import user_config_dir
from colorama import Fore, Style

gr = Fore.GREEN
rs = Style.RESET_ALL

class WalletCommand():
    def __init__(self):
        contract_addr_file_name = 'build/contract_address'
        if os.path.isfile(contract_addr_file_name):
            bounceable_addr = ""
            with open(contract_addr_file_name, 'r', encoding='utf-8') as file:
                addresses = file.read().split()
                bounceable_addr = addresses[2]
            logger.info(f"Your bounceable address is: {gr}{bounceable_addr}{rs}")

            deploy_wallet_addr_dir = user_config_dir('toncli')
            deploy_bouncable = ""
            with open(os.path.abspath(f"{deploy_wallet_addr_dir}/wallet/build/contract_address"), 'r',
                      encoding='utf-8') as file:
                addresses = file.read().split()
                deploy_bouncable = addresses[2]
            logger.info(f"Your deploy wallet address is: {gr}{deploy_bouncable}{rs}")
        else:
            logger.error(
                "Can't find file with address information.\n"
                "Its seems that you haven't built your wallet yet.\n"
                "You can do it with commands:\n"
                "'toncli build' - to build locally\n"
                "'toncli deploy' to build and immediately deploy it to net")
