from argparse import ArgumentParser
import shlex
import sys
from toncli.modules.deploy_contract import ContractDeployer
from toncli.modules.utils.system.argparse_fix import argv_fix

class DeployCommand():
    def __init__(self, string_kwargs, parser: ArgumentParser):
        _, kwargs = argv_fix(sys.argv, string_kwargs)
        args = parser.parse_args(['deploy', *kwargs])

        deployer = ContractDeployer(network=args.net, update_config=args.update,
                                    workchain=args.workchain,
                                    ton=args.ton,
                                    data_params=shlex.split(args.data_params))
        real_args, _ = argv_fix(sys.argv, string_kwargs)
        deployer.publish(real_args[2:])
        