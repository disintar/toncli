from argparse import ArgumentParser
import sys
from toncli.modules.abstract.deployer import AbstractDeployer
from toncli.modules.deploy_contract import ContractDeployer
from toncli.modules.utils.system.argparse_fix import argv_fix

class GetCommand():
    def __init__(self, string_kwargs, parser: ArgumentParser):
        real_args, kwargs = argv_fix(sys.argv, string_kwargs)
        args = parser.parse_args(['get', *kwargs])

        if args.address:
            class My:
                name = 'my-cool-smc'

            deployer = AbstractDeployer()
            deployer.network = args.net
            deployer.update_config = args.update

            deployer.get(real_args[2:], args, fake_addreses=[[My()], [[None, args.address]]])
        else:
            deployer = ContractDeployer(network=args.net, update_config=args.update)
            deployer.get(real_args[2:], args)
            