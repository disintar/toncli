import argparse
import textwrap

from colorama import Fore

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
{Fore.GREEN}   wallet - create project with v3 wallet example'''

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(help_text))

    subparser = parser.add_subparsers()

    parser_list = subparser.add_parser('startproject')
    parser_list.add_argument('project', default='wallet', choices=['wallet'])
    parser_list.add_argument("--name", "-n", default='wallet', type=str, help='New project folder name')

    args = parser.parse_args()

    if 'project' in args:
        bootstrapper = ProjectBootstrapper(project_name=args.project, folder_name=args.name)
        bootstrapper.deploy()


if __name__ == '__name__':
    main()
