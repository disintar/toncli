import argparse
import textwrap

from colorama import Fore, Style

from .modules.deploy import Deployer
from .modules.projects import ProjectBootstrapper


def main():
    '''
    CLI interface definition

    :return:
    '''

    help_text = f'''{Fore.YELLOW}TON blockchain is the future 🦄
--------------------------------
Command list, e.g. usage: fift-cli startproject wallet

{Fore.BLUE}startproject   
{Fore.GREEN}   wallet - create project with v3 wallet example

{Fore.BLUE}deploy   

{Style.RESET_ALL}
Each command have help e.g.: fift-cli deploy -h
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
    parser_deploy.add_argument("--configure", action='store_true',
                               help='Configurate deploy wallet')

    args = parser.parse_args()

    if 'project' in args:
        bootstrapper = ProjectBootstrapper(project_name=args.project, folder_name=args.name)
        bootstrapper.deploy()
    elif 'net' in args:
        deployer = Deployer(network=args.net, update_config=args.configure)


if __name__ == '__name__':
    main()
