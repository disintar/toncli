import os
import sys
from typing import Tuple

from colorama import Fore, Style

from fift_cli.modules.utils.conf import project_root
from fift_cli.modules.utils.fift import contract_manipulation, test_fift
from fift_cli.modules.utils.func import build as fift_build
from fift_cli.modules.utils.lite_client import get_account_status, send_boc
from fift_cli.modules.utils.log import logger

bl = Fore.CYAN
gr = Fore.GREEN
rs = Style.RESET_ALL


class AbstractDeployer:
    def __init__(self):
        self.update_config: bool = False
        self.address: str = ""
        self.network: str = ""
        self.workchain: int = 0
        self.project_root: str = ""

    def get_status(self) -> Tuple[float, bool]:
        """Get balance and inited state for Contract"""
        return get_account_status(self.network, self.address, update_config=self.update_config, cwd=self.project_root)

    def deploy(self):
        """Deploy Contract"""
        send_boc(self.network, f'{self.project_root}/build/boc/contract-create.boc', cwd=self.project_root,
                 update_config=self.update_config)

    def build(self):
        """Generate BOC of external message for project"""
        return contract_manipulation(f"{self.project_root}/build/code.fif",
                                     f"{self.project_root}/fift/data.fif",
                                     self.workchain, cwd=self.project_root)

    def get_address(self):
        """Get addres from address_text generated in contract_manipulation.fif"""

        if not os.path.exists(f"{self.project_root}/build/address_text"):
            raise ValueError(f"😥 No address_text found in {self.project_root}/build/address_text")

        with open(f"{self.project_root}/build/address_text") as f:
            address_text = f.read().split()

            if len(address_text) != 3:
                raise ValueError(f"😥 Strange data in {self.project_root}/build/address_text")

        return address_text

    def compile_func(self):
        """Compile func to code.fif"""

        # Build code
        fift_build(f"{self.project_root}/func/",
                   f"{self.project_root}/build/code.fif", cwd=self.project_root)

    def run_tests(self):
        # Run tests
        # CWD - Need to specify folder so keys saved to build/ (relative path in fift)
        test_fift(fift_files_locations=[f"{self.project_root}/fift/data.fif"],
                  test_file_path=f"{project_root}/fift_cli/modules/fift/run_test.fif",
                  cwd=self.project_root)

    def check_for_needed_files_to_deploy(self) -> bool:
        """Check needed files and log if there is no one"""

        files = os.listdir(self.project_root)
        needed_structure = {
            'func': ['code.fc', 'files.yaml'],
            'fift': ['data.fif'],
            'build': []
        }

        for folder in needed_structure:
            if folder not in files:
                logger.error(f"🚫 It is not project root, there is no folder {bl}{folder}{rs} - I can't deploy it")
                sys.exit()

            for file in needed_structure[folder]:
                folder_files = os.listdir(f"{self.project_root}/{folder}")

                if file not in folder_files:
                    logger.error(
                        f"🚫 It is not project root, there is no file {bl}{file}{rs} folder {bl}{folder}{rs} "
                        f"- I can't deploy it")
                    sys.exit()
        return True
