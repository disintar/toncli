import os
import sys

from colorama import Fore, Style
from toncli.modules.deploy_contract import ContractDeployer
from toncli.modules.utils.system.conf import getcwd
from toncli.modules.utils.system.log import logger

bl = Fore.CYAN
gr = Fore.GREEN
rs = Style.RESET_ALL

class AddrsCommand():
    def __init__(self):
        if 'project.yaml' not in os.listdir(getcwd()):
            logger.error(f"🚫 {gr}{getcwd()}{rs} is not project root, there is no file {bl}project.yaml{rs} file")
            sys.exit(0)

        contract = ContractDeployer(network='testnet')
        addrs = contract.get_address()

        for name, addr in zip(contract.project_config.contracts, addrs):
            logger.info(f"[{gr}{name.name}{rs}] 🦄 Raw address: {bl}{addr[0]}{rs}")
            logger.info(f"[{gr}{name.name}{rs}] 🦝 Bounceable address: {bl}{addr[1]}{rs}")
            logger.info(f"[{gr}{name.name}{rs}] 🐏 Non-bounceable address: {bl}{addr[2]}{rs}")
        sys.exit()
        