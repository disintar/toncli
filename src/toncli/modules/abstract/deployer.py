import os
import sys
import tempfile
from argparse import Namespace
from typing import List

from colorama import Fore, Style
from itertools import cycle
from time import sleep
from typing import Tuple

from toncli.modules.utils.fift.commands import contract_manipulation, test_fift
from toncli.modules.utils.func.commands import build as fift_build
from toncli.modules.utils.lite_client.commands import get_account_status, send_boc
from toncli.modules.utils.system.project import check_for_needed_files_to_deploy
from toncli.modules.utils.system.project_conf import TonProjectConfig
from toncli.modules.utils.system.log import logger
from toncli.modules.utils.fift.fift import Fift
from toncli.modules.utils.system.project_conf import ProjectConf
from toncli.modules.utils.ton.cell import deserialize
from toncli.modules.utils.lite_client.parser import split_get_output
from jinja2 import FileSystemLoader, Environment, select_autoescape

from toncli.modules.utils.lite_client.lite_client import LiteClient
from toncli.modules.utils.system.conf import project_root

bl = Fore.CYAN
gr = Fore.GREEN
rs = Style.RESET_ALL


class Cell:
    def __init__(self, data: str, refs: List['Cell']):
        self.data = data
        self.refs = refs

    def serialize(self):
        refs = [cell.serialize() for cell in self.refs]
        refs = [f"{ref} ref," for ref in refs]
        return f"<b {self.data} s, {' '.join(refs)} b>"


class AbstractDeployer:
    def __init__(self):
        self.update_config: bool = False
        self.addresses: List[str] = [""]
        self.network: str = ""
        self.workchain: int = 0
        self.project_root: str = ""
        self.project_config: ProjectConf = ...
        self.data_params: list = []

    def parse_contracts(self, kwargs):
        contracts = kwargs.contracts.split() if kwargs.contracts else None
        if contracts is not None and len(contracts) > 0:
            real_contracts = []

            for item in contracts:
                for config in self.project_config.contracts:
                    if config.name == item:
                        real_contracts.append(config)
        else:
            real_contracts = self.project_config.contracts

        return real_contracts

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

        data = []
        for contract in contracts:
            data.append(contract_manipulation(contract.to_save_location,
                                              contract.data,
                                              self.workchain,
                                              contract.boc,
                                              contract.address,
                                              cwd=self.project_root,
                                              data_params=self.data_params))
        return data

    def get_address(self, contracts: List[TonProjectConfig] = None) -> List[List[str]]:
        """Get addres from address_text generated in contract_manipulation.fif"""
        if not contracts:
            contracts = self.project_config.contracts

        addresses = []

        for contract in contracts:
            # TODO: load address from build/contract.addr
            if not os.path.exists(os.path.abspath(contract.address)):
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

    def run_tests(self, contracts: List[TonProjectConfig] = None):
        if not contracts:
            contracts = self.project_config.contracts

        for contract in contracts:
            # Run tests
            # CWD - Need to specify folder so keys saved to build/ (relative path in fift)
            test_fift(fift_files_locations=[contract.data],
                      test_file_path=f"run_test.fif.template",
                      cwd=self.project_root, data_params=self.data_params)

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
        logger.info("🐰 Getting seqno for transaction")
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

    def send(self, args: List[str], kwargs: Namespace, fake_addreses=False):
        if not fake_addreses:
            real_contracts = self.parse_contracts(kwargs)
        else:
            real_contracts = fake_addreses[0]

        names = ', '.join([i.name for i in real_contracts])

        logger.info(
            f"🤔 You want to send internal message to [{gr}{names}{rs}] from deploy-wallet"
            f" with amount [{bl}{kwargs.amount}{rs}]")

        balance, is_inited = self.deploy_contract.get_status()[0]

        if balance < kwargs.amount or not is_inited:
            logger.error(
                f"💰 Please, send more TON for deployment to [{gr}{self.deploy_contract.addresses[0][1]}{rs}] in"
                f" [{bl}{self.deploy_contract.network}{rs}]")
            sys.exit()

        if not fake_addreses:
            # Get contracts addresses
            self.addresses = self.get_address(real_contracts)
        else:
            self.addresses = fake_addreses[1]

        for address in self.addresses:
            seqno = self.deploy_contract.get_seqno()[0]
            args = [f'{self.deploy_contract.project_root}/fift/usage.fif', 'build/contract', address[1], '0',
                    str(seqno),
                    str(kwargs.amount)]

            if kwargs.body:
                if kwargs.body[0] != '/':  # not absolute path
                    args.extend(['-B', f"{os.getcwd()}/{kwargs.body}"])
                else:  # use absolute path
                    args.extend(['-B', f"{kwargs.body}"])

            if kwargs.force_bounce:
                args.append('--force-bounce')

            if kwargs.no_bounce:
                args.append('--no-bounce')

            if kwargs.mode:
                args.extend(['--mode', kwargs.mode])

            logger.info(f"Run command: {' '.join(args)}")

            fift = Fift('sendboc', args=args, kwargs={'fift_args': "",
                                                      'lite_client_args': "",
                                                      'build': False,
                                                      'net': self.network,
                                                      'update': False}, quiet=False,
                        cwd=self.deploy_contract.project_root)
            fift.run()

    def get(self, args: List[str], kwargs: Namespace, fake_addreses=False):
        """Run get methods on contracts"""
        # TODO: it wasn't good idea to parse lite client output
        # We can run get methods locally by runvm (savedata / saveaccount) and then get output / run fift
        # It's needed to be done this way

        if not fake_addreses:
            real_contracts = self.parse_contracts(kwargs)

            # Get contracts addresses
            self.addresses = self.get_address(real_contracts)
        else:
            real_contracts, self.addresses = fake_addreses

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
            if kwargs.fift and len(kwargs.fift) > 0:
                output = split_get_output(output)
                to_fift = []

                # TODO: use fift runvm
                # This is not right, but we have not time
                # This code is load C{...} from lite client to fift code
                for line in output:
                    # If cell hash present
                    if line[:2] == 'C{':
                        _hash = line[2:-1]

                        # we need to parse cell
                        lite_client = LiteClient('runmethod', args=[address[1], *args],
                                                 kwargs={'lite_client_args': '-v 0',
                                                         'net': self.network,
                                                         'update': self.update_config,
                                                         'lite_client_post_args': ["-c", f"dumpcell {_hash}"]},
                                                 get_output=True)
                        output_cells = lite_client.run_safe()

                        cells = []

                        append_other = False
                        # cell can contains references
                        for line in output_cells.split('\n'):
                            if append_other and len(line):
                                cells.append(line[2:])

                            if _hash.upper() in line and '} =' in line:
                                append_other = True

                        main_cell = None
                        for cell in cells:
                            level = len(cell) - len(cell.strip())

                            if level == 0:
                                main_cell = Cell(data=cell, refs=[])
                            else:
                                needed_cell: Cell = None

                                for current_level in range(level):
                                    if not needed_cell:
                                        needed_cell = main_cell
                                    else:
                                        needed_cell = needed_cell.refs[-1]

                                needed_cell.refs.append(Cell(data=cell.strip(), refs=[]))
                        to_fift.append(main_cell.serialize())
                    elif line[:3] == 'CS{':
                        # Дай бог здоровья больше не писать такой код
                        # И использовать fift runvm
                        # Но к несчастью я не догадался так сделать сначала
                        # А сейчас хочется сделать продакшн реди как можно быстрее
                        # Если кто-то это переделает - буду очень благодарен
                        # disintar.io

                        cell = line.split()[0].replace('CS{Cell{', '')[:-1]

                        cut = list(map(int, line.split()[2][:-1].split('..')))

                        bits = deserialize(cell, *cut)

                        bits = ["<b b{%s} s, b> <s" % bits[i:i + 128] for i in range(0, len(bits), 128)]
                        if len(bits) > 1:
                            bits = f'{bits[0]} {" |+ ".join(bits[1:])} |+'
                        else:
                            bits = bits[0]

                        to_fift.append(bits)
                    else:
                        to_fift.append(line)

                render_kwargs = {
                    'code': kwargs.fift,
                    'output': ' '.join(to_fift)
                }

                # Load template of transaction_debug
                loader = FileSystemLoader(f"{project_root}/modules/fift")

                env = Environment(
                    loader=loader,
                    autoescape=select_autoescape()
                )

                template = env.get_template("get_run.fif.template")

                rendered = template.render(**render_kwargs)

                temp_location: str = tempfile.mkstemp(suffix='.fif')[1]

                with open(temp_location, 'w') as f:
                    f.write(rendered)

                fift = Fift('run', args=[temp_location])
                fift.run()
            else:
                try:
                    output = int(output)
                    hex = "{0:x}".format(output)

                    string_output = bytearray.fromhex(hex).decode()
                    logger.info(f"🧐 Auto parse string: [ {string_output} ]")
                except Exception as e:
                    logger.error(f"🧐 Can't auto parse string")
