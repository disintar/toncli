from argparse import ArgumentParser
import sys
from toncli.modules.abstract.deployer import AbstractDeployer
from toncli.modules.deploy_contract import ContractDeployer
from toncli.modules.deploy_wallet_contract import DeployWalletContract
from toncli.modules.utils.system.argparse_fix import argv_fix

class SendCommand():
    def __init__(self, string_kwargs, parser: ArgumentParser):
        args = parser.parse_args()
        _, _ = argv_fix(sys.argv, string_kwargs)

        if args.address:
            class My:
                name = 'my-cool-smc'

            deployer = AbstractDeployer()
            deployer.network = args.net
            deployer.update_config = args.update
            deployer.deploy_contract = DeployWalletContract(args.net, 0)

            deployer.send([], args, fake_addreses=[[My()], [[None, args.address]]])
        else:
            deployer = ContractDeployer(network=args.net, update_config=args.update)
            deployer.send([], args)
