import os
import sys

from colorama import Fore, Style

from tncli.modules.abstract.deployer import AbstractDeployer
from tncli.modules.projects import ProjectBootstrapper
from tncli.modules.utils.conf import config_folder
from tncli.modules.utils.log import logger

bl = Fore.CYAN
gr = Fore.GREEN
rs = Style.RESET_ALL


class DeployWalletContract(AbstractDeployer):
    def __init__(self, network: str, workchain: int):
        """
        :param network: network to use
        :param workchain: working only whet deploy
        """
        super().__init__()
        self.network = network
        self.workchain = workchain
        self.project_root = f"{config_folder}/wallet"

        # We need to check if wallet for deploying is exist
        if 'wallet' not in os.listdir(config_folder):
            # If it's not existing we need to create it
            logger.info(
                f"✋ Do not panic - i'm creating wallet in {config_folder}, so you can easily manage your contracts")

            # deploy simple wallet
            pb = ProjectBootstrapper('wallet', 'wallet', config_folder)
            pb.deploy()

            # Compile func
            self.compile_func()

            # Run tests
            self.run_tests()

            # TODO: add custom workchain for DeployWallet
            data = self.build()
            logger.info(data)

            if data:
                logger.info(
                    f"🗝 You need to send TON to {gr}Bounceable address{rs} of Deployment wallet to start work\n"
                    f"💎 About {gr}2 TON{rs} will be OK for 10-12 contracts\n"
                    f"🧪 Test coins can be found in {bl}@testgiver_ton_bot{rs} / @tondev")

                sys.exit()
        else:
            address_text = self.get_address()
            self.address = address_text[1]
            balance, is_inited = self.get_status()

            logger.info(
                f"🦘 Found existing deploy-wallet [{gr}{address_text[1]}{rs}] (Balance: {balance}💎, "
                f"Is inited: {is_inited}) in {config_folder}")
            self.address = address_text[1]

    def send_ton(self, address: str, count: int):
        """Send ton to some address from DeployWallet"""
        balance, is_inited = self.get_status()

        if balance < count or not is_inited:
            logger.error(
                f"💰 Please, send more TON for deployment to [{gr}{self.address}{rs}] in [{bl}{self.network}{rs}]")
            sys.exit()


if __name__ == '__main__':
    DeployWalletContract('testnet', 0)
