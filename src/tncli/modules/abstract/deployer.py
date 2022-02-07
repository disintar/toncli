import os
import sys
from itertools import cycle
from time import sleep
from typing import Tuple, Optional, List

from colorama import Fore, Style

from tncli.modules.utils.system.conf import project_root
from tncli.modules.utils.fift.commands import contract_manipulation, test_fift
from tncli.modules.utils.func.commands import build as fift_build
from tncli.modules.utils.lite_client.commands import get_account_status, send_boc
from tncli.modules.utils.system.project import check_for_needed_files_to_deploy
from tncli.modules.utils.lite_client.lite_client import LiteClient
from tncli.modules.utils.system.log import logger
from tncli.modules.utils.system.project_conf import ProjectConf, TonProjectConfig

bl = Fore.CYAN
gr = Fore.GREEN
rs = Style.RESET_ALL


class AbstractDeployer:
    def __init__(self):
        self.update_config: bool = False
        self.addresses: List[str] = [""]
        self.network: str = ""
        self.workchain: int = 0
        self.project_root: str = ""
        self.project_config: ProjectConf = ...

    def get_status(self, addreses: List[List[str]] = None) -> List[Tuple[float, bool]]:
        """Get balance and inited state for Contract"""
        if not addreses:
            addreses = self.addresses
        statuses = []

        for address in addreses:
            statuses.append(
                get_account_status(self.network, address[1],
                                   update_config=self.update_config,
                                   cwd=self.project_root))
        return statuses

    def deploy(self, contracts: List[TonProjectConfig] = None):
        """Deploy Contract"""
        if not contracts:
            contracts = self.project_config.contracts

        statuses = self.get_status()

        for contract, (_, is_inited) in zip(contracts, statuses):
            if not is_inited:
                deploy_boc = send_boc(self.network, contract.boc, cwd=self.project_root,
                                      update_config=self.update_config, get_output=True)

                if 'error' in deploy_boc:
                    logger.error("🥵 Can't deploy boc...")
                    logger.error(deploy_boc)
                    sys.exit()
            else:
                logger.warning(f"🥰 Contract [{gr}{contract.name}{rs}] is already inited, pass")

    def build(self, contracts: List[TonProjectConfig] = None):
        """Generate BOC of external message for project"""

        if not contracts:
            contracts = self.project_config.contracts

        for contract in contracts:
            contract_manipulation(contract.to_save_location,
                                  contract.data,
                                  self.workchain,
                                  contract.boc,
                                  contract.address,
                                  cwd=self.project_root)

    def get_address(self, contracts: List[TonProjectConfig] = None) -> List[List[str]]:
        """Get addres from address_text generated in contract_manipulation.fif"""
        if not contracts:
            contracts = self.project_config.contracts

        addresses = []

        for contract in contracts:
            # TODO: load address from build/contract.addr
            if not os.path.exists(contract.address):
                raise ValueError(f"😥 No address_text found in {contract.address}")

            with open(contract.address) as f:
                address_text = f.read().split()

                if len(address_text) != 3:
                    raise ValueError(f"😥 Strange data in {contract.address}")
                addresses.append(address_text)

        return addresses

    def compile_func(self, contracts: List[TonProjectConfig] = None):
        """Compile func to code.fif"""
        # Build code
        fift_build(self.project_root, cwd=self.project_root, contracts=contracts)

    def run_tests(self, contracts: List[TonProjectConfig]):
        if not contracts:
            contracts = self.project_config.contracts

        for contract in contracts:
            # Run tests
            # CWD - Need to specify folder so keys saved to build/ (relative path in fift)
            test_fift(fift_files_locations=[contract.data],
                      test_file_path=f"{project_root}/modules/fift/run_test.fif",
                      cwd=self.project_root)

    def check_for_needed_files_to_deploy(self) -> bool:
        """Check if current root is project root"""
        return check_for_needed_files_to_deploy(self.project_root, True)

    def wait_for_deploy(self, contracts: List[TonProjectConfig] = None, only_balance=False,
                        addreses: List[List[str]] = None):
        """
        Check current deploy status

        :param addreses: need to pass if only_balance to correctly get status
        :param contracts: contracts to check
        :param only_balance: if only_balance passed - will check only non-zero balance
        :return:
        """
        if not addreses:
            addreses = self.addresses

        if not contracts:
            contracts = self.project_config.contracts

        is_deployed = 0
        statuses_emoji = cycle(["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"])

        while is_deployed != len(contracts):
            # TODO: fjx addreses, it's not a good solution here
            statuses = self.get_status(addreses)
            current_text_status = []
            is_deployed = 0
            status = next(statuses_emoji)

            for address, (balance, is_inited), contract in zip(addreses, statuses, contracts):
                text_status = f"[{status}] [{bl}{contract.name}{rs}] [{gr}{address[1]}{rs}] {balance}💎 / Inited: {gr}{is_inited}{rs}"
                current_text_status.append(text_status)

                if not only_balance:
                    if is_inited:
                        is_deployed += 1
                else:
                    if balance > 0:
                        is_deployed += 1

            if is_deployed != len(contracts):
                print("\r", current_text_status[is_deployed], end='')
                sleep(1)
            else:
                print("\r", current_text_status[is_deployed - 1], end='')
        print()  # add new line at the end
        logger.info(
            "🙀 All contracts successfully deployed!" if not only_balance else "🙀 All contracts now with non-zero balance")

    def get_seqno(self) -> List[int]:
        """Run runmethod on lite-client and parse seqno from answer"""

        seqnos = []
        for address in self.addresses:
            lite_client = LiteClient('runmethod', args=[address[1], 'seqno'], kwargs={'lite_client_args': '-v 0',
                                                                                      'net': self.network,
                                                                                      'update': False},
                                     get_output=True)
            output = lite_client.run_safe()

            output = output.split('\n')[-3]
            output = int(output[11:-2])
            seqnos.append(output)

        return seqnos
