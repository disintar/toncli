import os
from typing import Tuple

from colorama import Fore, Style

from .projects import ProjectBootstrapper
from .utils.conf import config_folder, project_root
from .utils.fift import test_fift, contract_manipulation
from .utils.func import build
from .utils.lite_client import get_account_status, send_boc
from .utils.log import logger

bl = Fore.CYAN
gr = Fore.GREEN
rs = Style.RESET_ALL


class DeployWalletContract:
    def __init__(self, network: str, workchain: int):
        """
        :param network: network to use
        :param workchain: working only whet deploy
        """
        self.network = network
        self.workchain = workchain

        # We need to check if wallet for deploying is exist
        if 'wallet' not in os.listdir(config_folder):
            # If it's not existing we need to create it
            logger.info(
                f"✋ Do not panic - i'm creating wallet in {config_folder}, so you can easily manage your contracts")

            # deploy simple wallet
            pb = ProjectBootstrapper('wallet', 'wallet', config_folder)
            pb.deploy()

            # Build code
            build(f"{config_folder}/wallet/func/",
                  f"{config_folder}/wallet/build/code.fif")

            # Run tests
            # CWD - Need to specify folder so keys saved to build/ (relative path in fift)
            test_fift(fift_files_locations=[f"{config_folder}/wallet/fift/data.fif"],
                      test_file_path=f"{project_root}/fift_cli/modules/fift/run_test.fif",
                      cwd=f"{config_folder}/wallet/")

            # TODO: add custom workchain for DeployWallet
            data = contract_manipulation(f"{config_folder}/wallet/build/code.fif",
                                         f"{config_folder}/wallet/fift/data.fif",
                                         0,
                                         cwd=f"{config_folder}/wallet/")

            if data:
                logger.info(
                    f"🗝 You need to send TON to {gr}Bounceable address{rs} of Deployment wallet to start work\n"
                    f"💎 About {gr}2 TON{rs} will be OK for 10-12 contracts\n"
                    f"🧪 Test coins can be found in {bl}@testgiver_ton_bot{rs} / @tondev")
        else:
            if not os.path.exists(f"{config_folder}/wallet/build/address_text"):
                raise ValueError(f"😥 No address_text found in {config_folder}/wallet/build/address_text")

            with open(f"{config_folder}/wallet/build/address_text") as f:
                address_text = f.read().split()

                if len(address_text) != 3:
                    raise ValueError(f"😥 Strange data in {config_folder}/wallet/build/address_text")

            logger.info(
                f"🦘 Found existing deploy-wallet [{gr}{address_text[1]}{rs}] in {config_folder}")
            self.address = address_text[1]

    def get_status(self) -> Tuple[float, bool]:
        """Get balance and inited state for DeployWallet"""
        return get_account_status(self.network, self.address)

    def deploy(self):
        """Deploy DeployWallet"""

        send_boc(self.network, f'{config_folder}/wallet/build/boc/contract-create.boc', f'{config_folder}/wallet/')

    def send_ton(self):
        """Send ton to some address from DeployWallet"""
        balance, is_inited = self.get_status()

        if balance > 0 and not is_inited:
            # deploy
            logger.info(f"🤑 Current balance is grater then 0: {gr}{balance}{rs} and "
                        f"wallet code is not deployed - so try to deploy")
            self.deploy()

        balance, is_inited = self.get_status()

        logger.info(f"💎 Current balance is: {gr}{balance}{rs} TON, Inited: {gr}{is_inited}{rs}")

        if balance == 0:
            logger.error(f"💰 Please, send more TON for deployment to [{gr}{self.address}{rs}]")
