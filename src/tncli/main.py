import argparse
import sys
import textwrap

from colorama import Fore, Style

from tncli.modules.deploy_contract import ContractDeployer
from tncli.modules.projects import ProjectBootstrapper
from tncli.modules.utils.argparse_fix import argv_fix
from tncli.modules.utils.fift import Fift

gr = Fore.GREEN
bl = Fore.CYAN
rs = Style.RESET_ALL


def main():
    '''
    CLI interface definition

    :return:
    '''

    help_text = f'''{Fore.YELLOW}TON blockchain is the future 🦄
--------------------------------
Command list, e.g. usage: tncli startproject wallet

{bl}startproject - create new project structure based on example project  
{gr}   wallet - create project with v3 wallet example

{bl}deploy - deploy current project to blockchain

{bl}fift / f - interact with fift :)
{gr}   interactive - default, run interactive fift
{gr}   run - run fift file ([config/fift-lib/] will be auto passed to -I
{gr}   sendboc - run fift file and run sendfile in lite-client, you need to set only BOC in the end of stack
             if it called in project root - will create build/boc/[filename].boc file, else will use temp dir

{bl}wallet - interact with deploy-wallet

{rs}
Each command have help e.g.: tncli deploy -h

Credits: andrey@head-labs.com / TON: EQCsCSLisPZ6xUtkgi_Tn5c-kipelVHRCxGdPu9x1gaVTfVC
'''

    # TODO: add logging verbose

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(help_text))

    subparser = parser.add_subparsers()

    parser_project = subparser.add_parser('startproject',
                                          description='Create new project structure based on example project')
    parser_project.add_argument('project', default='wallet', choices=['wallet'],
                                help="Which default project to bootstrap")

    parser_project.add_argument("--name", "-n", default='wallet', type=str, help='New project folder name')

    parser_deploy = subparser.add_parser('deploy', description='Deploy project to blockchain')
    parser_deploy.add_argument("--net", "-n", default='testnet', type=str, choices=['testnet', 'mainnet'],
                               help='Network to deploy')
    parser_deploy.add_argument("--workchain", "-wc", default=0, type=int, help='Workchain deploy to')
    parser_deploy.add_argument("--ton", "-t", default=0.05, type=int, help='How much TON will be sent to new contract')
    parser_deploy.add_argument("--update", action='store_true', help='Update cached configs of net')

    fift_help = f'''positional arguments:
  {bl}command{rs}              Which mode to run, can be [interactive, run, sendboc]
  {gr}   interactive - default, run interactive fift
  {gr}   run - run fift file ([config/fift-lib/] will be auto passed to -I
  {gr}   sendboc - run fift file and run sendfile in lite-client, you need to set only BOC in the stack
               if it called in project root - will create build/boc/[filename].boc file, else will use temp dir
  {rs}
'''
    subparser.add_parser('f', help="Same as fift",
                         formatter_class=argparse.RawDescriptionHelpFormatter,
                         description=textwrap.dedent(fift_help))
    subparser.add_parser('run', help="Same as fift run",
                         formatter_class=argparse.RawDescriptionHelpFormatter,
                         description=textwrap.dedent(fift_help))
    parser_fift = subparser.add_parser('fift', help=fift_help,
                                       formatter_class=argparse.RawDescriptionHelpFormatter,
                                       description=textwrap.dedent(fift_help))
    parser_fift.add_argument("--net", "-n", default='testnet', type=str, choices=['testnet', 'mainnet'],
                             help='Network to deploy')
    parser_fift.add_argument("--workchain", "-wc", default=0, type=int, help='Workchain deploy to')
    parser_fift.add_argument("--update", action='store_true', default=False, help='Update cached configs of net')
    parser_fift.add_argument("--fift-args", "-fa", type=str, default='',
                             help='Pass args to fift command, e.g.: -fa "-v 4" - '
                                  'set verbose level, will overwrite default ones, '
                                  'if you want pass args after command just don\'t use flag, f.e.g. '
                                  '[tncli fift run wallet.fif 0 0 1 -v 4]')
    parser_fift.add_argument("--lite-client-args", "-la", type=str,
                             default='',
                             help='Pass args to lite-client command in sendboc mode, '
                                  'e.g.: -la "-v 4" - set verbose level')
    command = sys.argv[1] if len(sys.argv) > 1 else None

    # wtf I need to do this, need to change!
    if command and command in ['fift', 'f', 'run'] and len(sys.argv) >= 2:
        _, kwargs = argv_fix(sys.argv)
        args = parser.parse_args(['fift', *kwargs])
    else:
        args = parser.parse_args()

    if len(args._get_kwargs()) == 0 and not command:
        parser.print_help()
        sys.exit(0)

    if command == 'startproject':
        bootstrapper = ProjectBootstrapper(project_name=args.project, folder_name=args.name)
        bootstrapper.deploy()

    elif command == 'deploy':
        deployer = ContractDeployer(network=args.net, update_config=args.update, workchain=args.workchain, ton=args.ton)
        deployer.publish()

    elif command == 'fift' or command == 'f' or command == 'run':
        # get real args
        real_args, _ = argv_fix(sys.argv)

        # Add support of tncli run ...
        if command != 'run':
            # Parse command (fift [command])
            command = real_args[2] if len(real_args) > 2 else None

        # Parse kwargs by argparse
        kwargs = dict(args._get_kwargs())

        fift = Fift(command, kwargs=kwargs, args=real_args[3:])
        fift.run()


if __name__ == '__name__':
    main()
