import os

from colorama import Fore, Style

from .projects import ProjectBootstrapper
from .utils.conf import config_folder
from .utils.log import logger
from .func import build

bl = Fore.BLUE
rs = Style.RESET_ALL


class DeployContract:
    def __init__(self):
        logger.info(f"🚀 You want to {bl}deploy{rs} your contract - that's grate!")

        if 'wallet' not in os.listdir(config_folder):
            logger.info(f"✋ Do not panic - i'm creating wallet in {config_folder}, so you can easily manage your contracts")

            # deploy simple wallet
            pb = ProjectBootstrapper('wallet', 'wallet', config_folder)
            pb.deploy()

            # So now we need to create external_message for contract
            build([f"{config_folder}/wallet/code.fc"], f"{config_folder}/wallet/build/code.fif")
