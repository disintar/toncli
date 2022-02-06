import os
import sys
import time
from typing import List

from colorama import Fore, Style

from tncli.modules.abstract.deployer import AbstractDeployer
from tncli.modules.deploy_wallet_contract import DeployWalletContract
from tncli.modules.utils.system.log import logger
from tncli.modules.utils.system.project import migrate_project_struction
from tncli.modules.utils.system.project_conf import ProjectConf

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

        # If files.yaml in func folder - it's older version of project structure, so migrate
        if os.path.exists(f"{self.project_root}/func/files.yaml"):
            migrate_project_struction('0.0.14', self.project_root)

        self.project_config = ProjectConf(self.project_root)
        self.ton = ton  # ton to send to smart contract
        self.workchain = workchain  # workchain deploy to

        # Check needed to deploy files
        self.check_for_needed_files_to_deploy()

        self.deploy_contract = DeployWalletContract(network, workchain)
        balance, is_inited = self.deploy_contract.get_status()[0]

        if not is_inited:
            if balance > 0:
                logger.info(f"🤑 Current balance is grater then 0: {gr}{balance}{rs} and "
                            f"wallet code is not deployed - so try to deploy")
                self.deploy_contract.build()
                self.deploy_contract.deploy()

                logger.info("😴 Sleep for 10 sec., wait while blockchain info will be updated")
                time.sleep(10)

            else:
                logger.error(
                    "🧓 Deployer contract is not inited yet, please send some TON there and then I can deploy project")
                sys.exit()

    def publish(self, contracts: List[str] = None):
        """Build, send ton, deploy contract"""

        logger.info(
            f"👻 Your smart contract project [{gr}{self.project_root}{rs}] "
            f"is now going to be {gr}deployed{rs}, get ready!")
        logger.info(f"🌈 Start building: ")
        if contracts is not None and len(contracts) > 0:
            real_contracts = []

            for item in contracts:
                for config in self.project_config.contracts:
                    if config.name == item:
                        real_contracts.append(config)
        else:
            real_contracts = self.project_config.contracts

        # Compile func
        self.compile_func(real_contracts)
        logger.info(f"🌲 Func compiled")

        self.run_tests(real_contracts)
        logger.info(f"🌲 Tests passed")

        # Build contracts
        self.build(real_contracts)
        logger.info(f"🌲 BOC created")

        # Get contracts addresses
        self.addresses = self.get_address(real_contracts)

        if self.ton > 0:
            for address, config in zip(self.addresses, real_contracts):
                logger.info(f"🌲 Sending TON to new contract [{bl}{config.name}{rs}] [{gr}{address[1]}{rs}]")

                # Send ton to this address
                self.deploy_contract.send_ton(address[1], self.ton, False)

            time.sleep(10)

        # Deploy current contract
        self.deploy(real_contracts)
        logger.info(f"💥 Deployed {gr}successfully{rs}!")

        statuses = self.get_status()

        for address, status, config in zip(self.addresses, statuses, real_contracts):
            logger.info(
                f"👾 Contract [{bl}{config.name}{rs}]  [{gr}{address[1]}{rs}] Balance: {status[0]}, is_inited: {status[1]}")

        logger.info(f"🚀 It may take some time to get is_inited to {gr}True{rs}")
