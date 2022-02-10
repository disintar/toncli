import os
import sys
import tempfile
from argparse import Namespace
from typing import List

from colorama import Fore, Style

from toncli.modules.abstract.deployer import AbstractDeployer
from toncli.modules.deploy_wallet_contract import DeployWalletContract
from toncli.modules.utils.system.log import logger
from toncli.modules.utils.fift.fift import Fift
from toncli.modules.utils.system.project import migrate_project_struction
from toncli.modules.utils.system.project_conf import ProjectConf
from toncli.modules.utils.ton.cell import deserialize
from toncli.modules.utils.lite_client.parser import split_get_output
from jinja2 import FileSystemLoader, Environment, select_autoescape

from toncli.modules.utils.lite_client.lite_client import LiteClient
from toncli.modules.utils.system.conf import project_root

gr = Fore.GREEN
bl = Fore.CYAN
rs = Style.RESET_ALL


class Cell:
    def __init__(self, data: str, refs: List['Cell']):
        self.data = data
        self.refs = refs

    def serialize(self):
        refs = [cell.serialize() for cell in self.refs]
        refs = [f"{ref} ref," for ref in refs]
        return f"<b {self.data} s, {' '.join(refs)} b>"


class ContractDeployer(AbstractDeployer):
    def __init__(self, network: str, update_config: bool = False, workchain: int = 0, ton: int = 0.05,
                 data_params: list = []):
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

        self.data_params = data_params if len(data_params) else [""]  # data which yuo want to store in nft

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
            if kwargs.fift and len(kwargs.fift) > 0:
                output = split_get_output(output)
                to_fift = []

                # TODO: use libtonlibjson.so
                # TODO: move to function, add descripion
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
                        # И использовать libtonlibjson.so
                        # Но к несчастью еще не готово это дело
                        # И хочется сделать продакшн реди уже сейчас
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

        self.wait_for_deploy(contracts=real_contracts)
