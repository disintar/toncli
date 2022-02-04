import os
import sys
from typing import Tuple, Optional

from colorama import Fore, Style

from tncli.modules.utils.system.conf import project_root
from tncli.modules.utils.fift.commands import contract_manipulation, test_fift
from tncli.modules.utils.func.commands import build as fift_build
from tncli.modules.utils.lite_client.commands import get_account_status, send_boc
from tncli.modules.utils.system.project import check_for_needed_files_to_deploy
from tncli.modules.utils.lite_client.lite_client import LiteClient
from tncli.modules.utils.system.log import logger

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

        deploy_boc = send_boc(self.network, f'{self.project_root}/build/boc/contract-create.boc', cwd=self.project_root,
                              update_config=self.update_config, get_output=True)

        if 'error' in deploy_boc:
            logger.error("🥵 Can't deploy boc...")
            logger.error(deploy_boc)
            sys.exit()

    def build(self):
        """Generate BOC of external message for project"""
        return contract_manipulation(f"{self.project_root}/build/code.fif",
                                     f"{self.project_root}/fift/data.fif",
                                     self.workchain, cwd=self.project_root)

    def get_address(self):
        """Get addres from address_text generated in contract_manipulation.fif"""

        # TODO: load address from build/contract.addr
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
                  test_file_path=f"{project_root}/tncli/modules/fift/run_test.fif",
                  cwd=self.project_root)

    def check_for_needed_files_to_deploy(self) -> bool:
        """Check if current root is project root"""
        return check_for_needed_files_to_deploy(self.project_root, True)

    def get_seqno(self) -> int:
        """Run runmethod on lite-client and parse seqno from answer"""

        lite_client = LiteClient('runmethod', args=[self.address, 'seqno'], kwargs={'lite_client_args': '-v 0',
                                                                                    'net': self.network,
                                                                                    'update': False},
                                 get_output=True)
        output = lite_client.run()

        if output:
            output = output.decode()

        if not output or 'result' not in output:
            logger.error("👻 There is a problem when trying to get seqno of wallet")
            logger.error("".join(output if output else "No output"))
            sys.exit()

        output = output.split('\n')[-3]
        output = int(output[11:-2])

        return output
