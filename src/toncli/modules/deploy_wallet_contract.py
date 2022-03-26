import os
import sys

from colorama import Fore, Style

from toncli.modules.abstract.deployer import AbstractDeployer
from toncli.modules.projects import ProjectBootstrapper
from toncli.modules.utils.system.conf import config_folder
from toncli.modules.utils.system.log import logger
from toncli.modules.utils.fift.fift import Fift
from toncli.modules.utils.system.project import migrate_project_struction
from toncli.modules.utils.system.project_conf import ProjectConf

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
        self.project_root = os.path.abspath(f"{config_folder}/wallet")

        # If files.yaml in func folder - it's older version of project structure, so migrate
        if os.path.exists(os.path.abspath(f"{self.project_root}/func/files.yaml")):
            migrate_project_struction('0.0.14', self.project_root)

        # We need to check if wallet for deploying is exist
        if 'wallet' not in os.listdir(config_folder):
            # If it's not existing we need to create it
            logger.info(
                f"✋ Do not panic - i'm creating wallet in {config_folder}, so you can easily manage your contracts")

            # deploy simple wallet
            pb = ProjectBootstrapper('wallet', 'wallet', config_folder)
            pb.deploy()

            self.project_config = ProjectConf(self.project_root)

            # Compile func
            self.compile_func()

            # Run tests
            self.run_tests()

            # TODO: add custom workchain for DeployWallet
            data = self.build()

            for i in data:
                logger.info(i)

            if len(data):
                logger.info(
                    f"🗝 You need to send TON to {gr}Bounceable address{rs} of Deployment wallet to start work\n"
                    f"💎 About {gr}2 TON{rs} will be OK for 10-12 contracts\n"
                    f"🧪 Test coins can be found in {bl}@testgiver_ton_bot{rs} / @tondev")

                sys.exit()
        else:
            self.project_config = ProjectConf(self.project_root)

            self.addresses = self.get_address()
            balance, is_inited = self.get_status()[0]

            logger.info(
                f"🦘 Found existing deploy-wallet [{gr}{self.addresses[0][1]}{rs}] (Balance: {balance}💎, "
                f"Is inited: {is_inited}) in {config_folder}")

    def send_ton(self, address: str, amount: float, quiet: bool = False):
        """Send ton to some address from DeployWallet"""
        balance, is_inited = self.get_status()[0]

        if balance < amount or not is_inited:
            logger.error(
                f"💰 Please, send more TON for deployment to [{gr}{self.address}{rs}] in [{bl}{self.network}{rs}]")
            sys.exit()

        seqno = self.get_seqno()[0]
        args = [os.path.abspath(f'{self.project_root}/fift/usage.fif'), 'build/contract', address, '0', str(seqno), str(amount),
                "--no-bounce"]

        fift = Fift('sendboc', args=args, kwargs={'fift_args': "",
                                             'lite_client_args': "",
                                             'build': False,
                                             'net': self.network,
                                             'update': False}, quiet=quiet, cwd=self.project_root)
        fift.run()


if __name__ == '__main__':
    DeployWalletContract('testnet', 0)
