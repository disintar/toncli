import os

from colorama import Fore, Style

from .projects import ProjectBootstrapper
from .utils.conf import config_folder, project_root
from .utils.fift import test_fift
from .utils.func import build
from .utils.log import logger

bl = Fore.CYAN
rs = Style.RESET_ALL


class DeployWalletContract:
    def __init__(self):
        # We need to check if wallet for deploying is exist
        if 'wallet' not in os.listdir(config_folder):
            # If it's not existing we need to create it
            logger.info(
                f"✋ Do not panic - i'm creating wallet in {config_folder}, so you can easily manage your contracts")

            # deploy simple wallet
            pb = ProjectBootstrapper('wallet', 'wallet', config_folder)
            pb.deploy()

            # Build code
            build(f"{config_folder}/wallet/func/", f"{config_folder}/wallet/build/code.fif")

            # Run tests
            test_fift(fift_files_locations=[f"{config_folder}/wallet/fift/data.fif"],
                      test_file_path=f"{project_root}/fift_cli/modules/fift/run_test.fif")
