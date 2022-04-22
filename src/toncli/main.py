import argparse
import sys
import textwrap
import configparser
from colorama import Fore, Style

from toncli.modules.utils.commands.commands_executer import CommandsExecuter
from toncli.modules.utils.system.conf import config_file
from toncli.modules.utils.system.log import logger
from toncli.modules.utils.check_hash import check_2_libs_actual, get_libs_paths

gr = Fore.GREEN
bl = Fore.CYAN
rs = Style.RESET_ALL

def main():
    '''
    CLI interface definition

    :return:
    '''

    fift_help = f'''positional arguments:
      {bl}command{rs}              Which mode to run, can be [interactive, run, sendboc]
      {gr}   interactive - default, run interactive fift
      {gr}   run - run fift file ([config/fift-lib/] will be auto passed to -I
      {gr}   sendboc - run fift file and run sendfile in lite-client, you need to set only BOC in the stack
                   if it called in project root - will create build/boc/[filename].boc file, else will use temp dir
      {rs}
    '''
    lite_client_help = f'''positional arguments:
          {bl}command{rs}             
          {gr}   interactive - default, run interactive lite_client
          {gr}   
          {gr}   OTHER - all other arguments will passed to lite_client e.g. tnctl lc help
          {rs}
        '''
    func_help = f'''positional arguments:
          {bl}command{rs}             
          {gr}   build - default, build func code in build/ folder, or just build func file 
          {gr}   
          {gr}   OTHER - all other arguments and kwargs will pass to fun command
          {rs}
        '''

    help_text = f'''{Fore.YELLOW}TON blockchain is the future 🦄
--------------------------------
Command list, e.g. usage: toncli start wallet

{bl}start - create new project structure based on example project  
{gr}   wallet - create project with v3 wallet example
{gr}   external_data - create external data usage example
{gr}   external_code - create external code usage example

{bl}deploy - deploy current project to blockchain
{bl}get - run get method on contract
{bl}run_transaction - run remote transaction locally

{bl}fift / f - interact with fift :)
{gr}   interactive - default, run interactive fift
{gr}   run - run fift file ([config/fift-lib/] will be auto passed to -I
{gr}   sendboc - run fift file and run sendfile in lite-client, to made this work you need to add `saveboc` at the end of file
             if it called in project root - will create build/boc/[filename].boc file, else will use temp dir

{bl}lite-client / lc - interact with lite-client :)
{gr}   interactive - default, run interactive lite-client
{gr}   
{gr}   All other commands will pass to lite-client -c (network config will auto pass to command)
{gr}   e.g. -> toncli lc help

{bl}func / fc - interact with func :)
{gr}   build - run build on file or project, will be auto passed stdlib

{gr}   All other commands will pass to func

{bl}tointeger - parse string to integer to pass to contract in func

{bl}sendboc - send file with boc info
{gr}   "sendboc <path-to-file.boc>" - sends BOC file
{gr}   "sendboc <path-to=file.fif> <other-params>" -  run fift file and run sendfile in lite-client (just like command "fift sendboc ...")

{bl}wallet - print addresses of 2 wallets - bounceable wallet and deploy wallet
{gr}   You can use this command only when wallet is built with commands "toncli build" or "toncli deploy"

All commands can be found in https://github.com/disintar/toncli/blob/master/docs/commands.md

{rs}
Each command have help e.g.: toncli deploy -h

Credits: {gr}disintar.io{rs} team
'''
    # This is concept of nft https://disintar.io
    # Nft information parse will be added in next versions of CLI
    # print("disintar.io NFT owners today say: 🙈 🙉 🙊")

    # TODO: add logging verbose
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(help_text))
    parser.add_argument("-v", "--version", help="package version", action='store_true')
    subparser = parser.add_subparsers()

    config = configparser.ConfigParser()
    config.read(config_file)
    config_default = config['DEFAULT']

    warn = config_default.get('LIBS_WARNING') != 'False'

    if warn:
        if not check_2_libs_actual():
            local_lib_path, global_lib_path = get_libs_paths()
            logger.warning(
                f"""\nIts seems that your local fift and func libs ({local_lib_path}) differs from their actual versions ({global_lib_path}). 
You can update them automatically using "toncli update_libs" or disable this warning by changing "LIBS_WARNING" to "False" param in cofig\n\n"""
            )
    #
    # START
    #

    parser_project = subparser.add_parser('start',
                                          description='Create new project structure based on example project')
    parser_project.add_argument('project', choices=['wallet', 'external_data', 'external_code'],
                                help="Which default project to bootstrap")

    parser_project.add_argument("--name", "-n", default=None, type=str, help='New project folder name')

    #
    # DEPLOY
    #

    parser_deploy = subparser.add_parser('deploy', description='Deploy project to blockchain')
    parser_deploy.add_argument("--net", "-n", default='testnet', type=str, choices=['testnet', 'mainnet', 'ownnet'],
                               help='Network to deploy')
    parser_deploy.add_argument("--workchain", "-wc", default=0, type=int, help='Workchain deploy to')
    parser_deploy.add_argument("--ton", "-t", default=0.05, type=float,
                               help='How much TON will be sent to new contract')
    parser_deploy.add_argument("--update", action='store_true', help='Update cached configs of net')
    parser_deploy.add_argument('--data-params', help='Data which you want to pass to data of your smart-contract',
                               default="", type=str)

    #
    # get
    #

    parser_get = subparser.add_parser('get', description='Deploy project to blockchain')
    parser_get.add_argument("--net", "-n", default='testnet', type=str, choices=['testnet', 'mainnet', 'ownnet'],
                            help='Network to deploy')
    parser_get.add_argument("--update", action='store_true', help='Update cached configs of net')
    parser_get.add_argument("--contracts", "-c", type=str,
                            help='Set contract name from project.yaml to run getmethod on')
    parser_get.add_argument("--address", "-a", type=str,
                            help='Set contract address to run get method on')
    parser_get.add_argument("--fift", "-f", type=str,
                            help='Run fift script on get output. Get output will be loaded to stack')

    #
    # send
    #

    parser_send = subparser.add_parser('send', description='Send internal transaction from deploy wallet to smc')
    parser_send.add_argument("--amount", "-a", type=float, default=0, help='How much TON need to send')
    parser_send.add_argument("--contracts", "-c", type=str, help='Set contract name from project.yaml to send to')
    parser_send.add_argument("--net", "-n", default='testnet', type=str, choices=['testnet', 'mainnet', 'ownnet'],
                             help='Network to use')
    parser_send.add_argument("--update", action='store_true', help='Update cached configs of net')
    parser_send.add_argument("--address", type=str,
                             help='Set contract address to run get method on')

    parser_send.add_argument("--mode", type=int, help='Sets transfer mode (0..255) for SENDRAWMSG')
    parser_send.add_argument("--body", "-b", type=str,
                             help='Path to fift file to get body from (need to set cell in the end of stack)')
    parser_send.add_argument("--no-bounce", "-nb", type=int, help='Clears bounce flag')
    parser_send.add_argument("--force-bounce", "-fb", type=int, help='Forces bounce flag')

    #
    # tointeger
    #

    subparser.add_parser('tointeger', description='Encode string to hex, than to integer')

    #
    # run_transaction
    #
    parser_run_transaction = subparser.add_parser('run_transaction',
                                                  description='Message debug - by lt / transaction hash / '
                                                              'smart contract address'
                                                              ' - run message locally and get stack error')
    parser_run_transaction.add_argument("logical_time", type=str)
    parser_run_transaction.add_argument("transaction_hash", type=str)
    parser_run_transaction.add_argument("smc_address", type=str)
    parser_run_transaction.add_argument("--net", "-n", default='testnet', type=str,
                                        choices=['testnet', 'mainnet', 'ownnet'],
                                        help='Network to run transaction')
    parser_run_transaction.add_argument("--function", "-f", default=-1, type=int,
                                        help='Function selector on runvm (-1 - external message, 0 - internal, ...')
    parser_run_transaction.add_argument("--save", "-s", default=None, type=str,
                                        help='Pass save location, so runvm script will not run and just save to '
                                             'your location')
    #
    # shortcuts
    #

    subparser.add_parser('f', help="Same as fift",
                         formatter_class=argparse.RawDescriptionHelpFormatter,
                         description=textwrap.dedent(fift_help))
    subparser.add_parser('fc', help="Same as func",
                         formatter_class=argparse.RawDescriptionHelpFormatter,
                         description=textwrap.dedent(func_help))
    subparser.add_parser('lc', help="Same as lite-client",
                         formatter_class=argparse.RawDescriptionHelpFormatter,
                         description=textwrap.dedent(lite_client_help))
    subparser.add_parser('run', help="Same as fift run",
                         formatter_class=argparse.RawDescriptionHelpFormatter,
                         description=textwrap.dedent(fift_help))
    subparser.add_parser('build', help="Same as func build",
                         formatter_class=argparse.RawDescriptionHelpFormatter,
                         description=textwrap.dedent(fift_help))

    #
    #  FIFT
    #

    parser_fift = subparser.add_parser('fift', help=fift_help,
                                       formatter_class=argparse.RawDescriptionHelpFormatter,
                                       description=textwrap.dedent(fift_help))
    parser_fift.add_argument("--net", "-n", default='testnet', type=str, choices=['testnet', 'mainnet', 'ownnet'],
                             help='Network to deploy')
    parser_fift.add_argument("--workchain", "-wc", default=0, type=int, help='Workchain deploy to')
    parser_fift.add_argument("--update", action='store_true', default=False, help='Update cached configs of net')
    parser_fift.add_argument("--build", action='store_true', default=False,
                             help='Build func code from func/ folder in project')
    parser_fift.add_argument("--fift-args", "-fa", type=str, default='',
                             help='Pass args and kwargs to fift command, e.g.: -fa "-v 4" - '
                                  'set verbose level, will overwrite default ones, '
                                  'if you want pass args after command just don\'t use flag, f.e.g. '
                                  '[toncli fift run wallet.fif 0 0 1 -v 4]')
    parser_fift.add_argument("--lite-client-args", "-la", type=str,
                             default='',
                             help='Pass args and kwargs to lite-client command in sendboc mode, '
                                  'e.g.: -la "-v 4" - set verbose level')

    #
    #  LITE CLIENT
    #

    parser_lite_client = subparser.add_parser('lite-client', help=lite_client_help,
                                              formatter_class=argparse.RawDescriptionHelpFormatter,
                                              description=textwrap.dedent(lite_client_help))
    parser_lite_client.add_argument("--net", "-n", default='testnet', type=str,
                                    choices=['testnet', 'mainnet', 'ownnet'],
                                    help='Network to deploy')
    parser_lite_client.add_argument("--update", action='store_true', default=False, help='Update cached configs of net')
    parser_lite_client.add_argument("--lite-client-args", "-la", type=str,
                                    default='',
                                    help='Pass args and kwargs to lite-client command at the start')
    parser_lite_client.add_argument("--lite-client-post-args", "-lpa", type=str,
                                    default='',
                                    help='Pass args to lite-client command at the end')

    #
    #  SEND BOC
    #
    parser_sendboc = subparser.add_parser('sendboc')
    parser_sendboc.add_argument('file', type=argparse.FileType('r'))
    parser_sendboc.add_argument("--net", "-n", default='testnet', type=str, choices=['testnet', 'mainnet', 'ownnet'],
                                help='Network to deploy')

    #
    #  WALLET
    #
    wallet = subparser.add_parser('wallet')

    #
    #  TESTS
    #
    run_tests = subparser.add_parser('run_tests')
    run_tests.add_argument("--contracts", "-c", type=str,
                           help='Set contract name from project.yaml to run tests on')
    run_tests.add_argument("--verbose", "-v", type=int, default=0,
                           help='Set contract name from project.yaml to run tests on')
    run_tests.add_argument("--output-results", "-o", action='store_true',
                           help='Set contract name from project.yaml to run tests on')

    #
    #  UPDATE LIBS
    #
    parser_update_libs = subparser.add_parser('update_libs')

    #
    #  FUNC
    #

    parser_func = subparser.add_parser('func', help=func_help,
                                       formatter_class=argparse.RawDescriptionHelpFormatter,
                                       description=textwrap.dedent(func_help))
    parser_func.add_argument("--func-args", "-fca", type=str,
                             default='',
                             help='Pass arguments to func command')
    parser_func.add_argument("--fift-args", "-fa", type=str, default='',
                             help='Pass args and kwargs to fift command, e.g.: -fa "-v 4" - '
                                  'set verbose level, will overwrite default ones, '
                                  'if you want pass args after command just don\'t use flag, f.e.g. '
                                  '[toncli fift run wallet.fif 0 0 1 -v 4]')
    parser_func.add_argument("--run", "-r", action='store_true', default=False,
                             help='Run fift code that was generated in build mode')

    # it's tricky one
    # we want to support arguments as by default is None
    # we can't do it with argparse
    # so we need to get all str flags to correctly parse kwargs after argument can be none by default
    string_kwargs = []

    group_actions = parser._subparsers._group_actions

    for group_action in group_actions:
        choices = group_action.choices

        for choice in choices:
            arguments = choices[choice]._option_string_actions

            for key in arguments:
                if arguments[key].type in [str, int, float]:
                    string_kwargs.append(key)

    #execute the command part
    command = sys.argv[1] if len(sys.argv) > 1 else None
    CommandsExecuter(command, string_kwargs, parser)

if __name__ == '__main__':
    main()
