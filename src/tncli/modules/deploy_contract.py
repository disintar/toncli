import os
import sys
import time

from colorama import Fore, Style

from tncli.modules.abstract.deployer import AbstractDeployer
from tncli.modules.deploy_wallet_contract import DeployWalletContract
from tncli.modules.utils.system.log import logger

gr = Fore.GREEN
bl = Fore.CYAN
rs = Style.RESET_ALL


class ContractDeployer(AbstractDeployer):
    def __init__(self, network: str, update_config: bool = False, workchain: int = 0, ton: int = 0.05):
        super().__init__()
        logger.info(f"🚀 You want to {bl}deploy{rs} your contract to {gr}{network}{rs} - that's grate!")

        self.network: str = network
        self.update_config: bool = update_config
        self.project_root: str = os.getcwd()
        self.ton = ton  # ton to send to smart contract
        self.workchain = workchain  # workchain deploy to

        # Check needed to deploy files
        self.check_for_needed_files_to_deploy()

        self.deploy_contract = DeployWalletContract(network, workchain)
        balance, is_inited = self.deploy_contract.get_status()

        if not is_inited:
            if balance > 0:
                logger.info(f"🤑 Current balance is grater then 0: {gr}{balance}{rs} and "
                            f"wallet code is not deployed - so try to deploy")
                self.deploy_contract.deploy()

                logger.info("😴 Sleep for 5 sec., wait while blockchain info will be updated")
                time.sleep(5)

            else:
                logger.error(
                    "🧓 Deployer contract is not inited yet, please send some TON there and then I can deploy project")
                sys.exit()

    def publish(self):
        """Build, send ton, deploy contract"""

        logger.info(
            f"👻 Your smart contract project [{gr}{self.project_root}{rs}] "
            f"is now going to be {gr}deployed{rs}, get ready!")
        logger.info(f"🌈 Start building: ")

        # Compile func
        self.compile_func()
        logger.info(f"🌲 Func compiled")

        self.run_tests()
        logger.info(f"🌲 Tests passed")

        # Build contract
        self.build()
        logger.info(f"🌲 BOC created")

        # Get contract address
        address_text = self.get_address()

        # Send ton to this address
        self.deploy_contract.send_ton(address_text[1], self.ton)
        logger.info(f"🌲 TON sended to new contract")

        # Deploy current contract
        data = self.deploy()
        logger.info(data)

        logger.info(f"💥 Deployed {gr}successfully{rs}!")

        balance, is_inited = self.get_status()

        logger.info(f"👾 Contract [{gr}{address_text[1]}{rs}] Balance: {balance}, is_inited: {is_inited}")


