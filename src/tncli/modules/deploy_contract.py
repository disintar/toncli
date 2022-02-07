import os
import sys
import time
from argparse import Namespace
from typing import List, Dict

from colorama import Fore, Style

from tncli.modules.abstract.deployer import AbstractDeployer
from tncli.modules.deploy_wallet_contract import DeployWalletContract
from tncli.modules.utils.system.log import logger
from tncli.modules.utils.system.project import migrate_project_struction
from tncli.modules.utils.lite_client.lite_client import LiteClient
from tncli.modules.utils.system.project_conf import ProjectConf

gr = Fore.GREEN
bl = Fore.CYAN
rs = Style.RESET_ALL


class ContractDeployer(AbstractDeployer):
    def __init__(self, network: str, update_config: bool = False, workchain: int = 0, ton: int = 0.05):
        super().__init__()

        self.network: str = network
        self.update_config: bool = update_config
        self.project_root: str = os.getcwd()

        # If files.yaml in func folder - it's older version of project structure, so migrate
        if os.path.exists(f"{self.project_root}/func/files.yaml"):
            migrate_project_struction('0.0.14', self.project_root)

        self.project_config = ProjectConf(self.project_root)
        logger.info(
            f"🚀 You want to {bl}interact{rs} with your contracts {gr}{[i.name for i in self.project_config.contracts]}{rs} in {gr}{network}{rs} - that's grate!")
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

                logger.info("😴  Wait while blockchain info will be updated:")
                self.deploy_contract.wait_for_deploy()

            else:
                logger.error(
                    "🧓 Deployer contract is not inited yet, please send some TON there and then I can deploy project")
                sys.exit()

    def get(self, args: List[str], kwargs: Namespace):
        """Run get methods on contracts"""
        contracts = kwargs.contracts.split() if kwargs.contracts else None
        if contracts is not None and len(contracts) > 0:
            real_contracts = []

            for item in contracts:
                for config in self.project_config.contracts:
                    if config.name == item:
                        real_contracts.append(config)
        else:
            real_contracts = self.project_config.contracts

        # Get contracts addresses
        self.addresses = self.get_address(real_contracts)

        for address, contract in zip(self.addresses, real_contracts):
            logger.info(f"👯 [{bl}{contract.name}{rs}] [{gr}{address[1]}{rs}] runmethod {args}")
            lite_client = LiteClient('runmethod', args=[address[1], *args], kwargs={'lite_client_args': '-v 0',
                                                                                    'net': self.network,
                                                                                    'update': self.update_config},
                                     get_output=True)
            output = lite_client.run_safe()
            output = output.split('\n')[-3]
            output = output[11:-2]

            logger.info(f"🧐 Output: [ {output} ]")

            try:
                output = int(output)
                string_output = bytearray.fromhex("{0:x}".format(output)).decode()
                logger.info(f"🧐 Auto parse sting: [ {string_output} ]")
            except Exception as e:
                logger.error(f"🧐 Can't auto parse string")

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
                self.wait_for_deploy(contracts=[config], only_balance=True, addreses=[address])

        # Deploy current contract
        self.deploy(real_contracts)
        logger.info(f"💥 Deployed {gr}successfully{rs}!")

        logger.info(f"🚀 It may take some time to get is_inited to {gr}True{rs}")

        self.wait_for_deploy(contracts=contracts)
