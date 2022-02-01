import argparse
import textwrap

from colorama import Fore, Style

from .modules.deploy_contract import ContractDeployer
from .modules.projects import ProjectBootstrapper


def main():
    '''
    CLI interface definition

    :return:
    '''

    help_text = f'''{Fore.YELLOW}TON blockchain is the future 🦄
--------------------------------
Command list, e.g. usage: fift-cli startproject wallet

{Fore.CYAN}startproject   
{Fore.GREEN}   wallet - create project with v3 wallet example

{Fore.CYAN}deploy   
{Fore.CYAN}wallet   

{Style.RESET_ALL}
Each command have help e.g.: fift-cli deploy -h

Credits: andrey@head-labs.com / TON: EQCsCSLisPZ6xUtkgi_Tn5c-kipelVHRCxGdPu9x1gaVTfVC
'''

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(help_text))

    subparser = parser.add_subparsers()

    parser_project = subparser.add_parser('startproject')
    parser_project.add_argument('project', default='wallet', choices=['wallet'],
                                help="Which default project to bootstrap")

    parser_project.add_argument("--name", "-n", default='wallet', type=str, help='New project folder name')

    parser_deploy = subparser.add_parser('deploy')
    parser_deploy.add_argument("--net", "-n", default='testnet', type=str, choices=['testnet', 'mainnet'],
                               help='Network to deploy')
    parser_deploy.add_argument("--workchain", "-wc", default=0, type=int, help='Workchain deploy to')
    parser_deploy.add_argument("--ton", "-t", default=0.05, type=int, help='How much TON will be sent to new contract')
    parser_deploy.add_argument("--update", action='store_true', help='Update cached configs of net')

    args = parser.parse_args()
    print(args)

    if 'project' in args:
        bootstrapper = ProjectBootstrapper(project_name=args.project, folder_name=args.name)
        bootstrapper.deploy()
    elif 'net' in args:
        deployer = ContractDeployer(network=args.net, update_config=args.update, workchain=args.workchain, ton=args.ton)
        deployer.publish()


if __name__ == '__name__':
    main()
