# Copyright (c) 2022 Disintar LLP Licensed under the Apache License Version 2.0

import argparse
import textwrap
from typing import Any
from toncli.modules.utils.text.text_utils import TextUtils
from toncli.modules.utils.system.conf import get_projects


class ParserUtil():
    subparser: Any

    def __init__(self, parser):
        self.subparser = parser.add_subparsers()

    def set_all_parsers(self):
        self.set_project_parser()
        self.set_deploy_parser()
        self.set_get_parser()
        self.set_send_parser()
        self.set_tointeger_parser()
        self.set_runtransation_parser()
        self.set_fift_parser()
        self.set_liteclient_parser()
        self.set_wallet_parser()
        self.set_runtests_parser()
        self.set_updatelibs_parser()
        self.set_func_parser()

    # define the function blocks
    def set_project_parser(self):
        parser_project = self.subparser.add_parser('start',
                                                   description='Create new project structure based on example project')
        parser_project.add_argument('project', choices=get_projects(),
                                    help="Which default project to bootstrap")

        parser_project.add_argument("--name", "-n", default=None, type=str, help='New project folder name')

    def set_deploy_parser(self):
        parser_deploy = self.subparser.add_parser('deploy',
                                                  description='Deploy project to blockchain, specify contract_name after command if special contract needed')
        parser_deploy.add_argument("--net", "-n", default='testnet', type=str, choices=['testnet', 'mainnet', 'ownnet'],
                                   help='Network to deploy')
        parser_deploy.add_argument("--workchain", "-wc", default=0, type=int, help='Workchain deploy to')
        parser_deploy.add_argument("--ton", "-t", default=0.05, type=float,
                                   help='How much TON will be sent to new contract')
        parser_deploy.add_argument("--update", action='store_true', help='Update cached configs of net')
        parser_deploy.add_argument('--data-params', help='Data which you want to pass to data of your smart-contract',
                                   default="", type=str)

    def set_get_parser(self):
        parser_get = self.subparser.add_parser('get', description='Run get method on contract')
        parser_get.add_argument("--net", "-n", default='testnet', type=str, choices=['testnet', 'mainnet', 'ownnet'],
                                help='Network to deploy')
        parser_get.add_argument("--update", action='store_true', help='Update cached configs of net')
        parser_get.add_argument("--contracts", "-c", type=str,
                                help='Set contract name from project.yaml to run getmethod on')
        parser_get.add_argument("--address", "-a", type=str,
                                help='Set contract address to run get method on')
        parser_get.add_argument("--fift", "-f", type=str,
                                help='Run fift script on get output. Get output will be loaded to stack')

    def set_send_parser(self):
        parser_send = self.subparser.add_parser('send', description='Send internal transaction from deploy wallet to smc')
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

    def set_tointeger_parser(self):
        self.subparser.add_parser('tointeger', description='Encode string to hex, than to integer')

    def set_runtransation_parser(self):
        parser_run_transaction = self.subparser.add_parser('run_transaction',
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

    def set_shorcuts_parser(self):
        self.subparser.add_parser('f', help="Same as fift",
                                  formatter_class=argparse.RawDescriptionHelpFormatter,
                                  description=textwrap.dedent(TextUtils.FIFT_HELP))
        self.subparser.add_parser('fc', help="Same as func",
                                  formatter_class=argparse.RawDescriptionHelpFormatter,
                                  description=textwrap.dedent(TextUtils.FUNC_HELP))
        self.subparser.add_parser('lc', help="Same as lite-client",
                                  formatter_class=argparse.RawDescriptionHelpFormatter,
                                  description=textwrap.dedent(TextUtils.LITE_CLIENT_HELP))
        self.subparser.add_parser('run', help="Same as fift run",
                                  formatter_class=argparse.RawDescriptionHelpFormatter,
                                  description=textwrap.dedent(TextUtils.FIFT_HELP))
        self.subparser.add_parser('build', help="Same as func build",
                                  formatter_class=argparse.RawDescriptionHelpFormatter,
                                  description=textwrap.dedent(TextUtils.FIFT_HELP))

    def set_fift_parser(self):
        parser_fift = self.subparser.add_parser('fift', help=TextUtils.FIFT_HELP,
                                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                                description=textwrap.dedent(TextUtils.FIFT_HELP))
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

    def set_liteclient_parser(self):
        parser_lite_client = self.subparser.add_parser('lite-client', help=TextUtils.LITE_CLIENT_HELP,
                                                       formatter_class=argparse.RawDescriptionHelpFormatter,
                                                       description=textwrap.dedent(TextUtils.LITE_CLIENT_HELP))
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

    def set_sendboc_parser(self):
        parser_sendboc = self.subparser.add_parser('sendboc')
        parser_sendboc.add_argument('file', type=argparse.FileType('r'))
        parser_sendboc.add_argument("--net", "-n", default='testnet', type=str, choices=['testnet', 'mainnet', 'ownnet'],
                                    help='Network to deploy')

    def set_wallet_parser(self):
        self.subparser.add_parser('wallet')

    def set_runtests_parser(self):
        run_tests = self.subparser.add_parser('run_tests')
        run_tests.add_argument("--contracts", "-c", type=str,
                               help='Set contract name from project.yaml to run tests on')
        run_tests.add_argument("tests", nargs='*',
                               help='Execute specific test(s) by name or mask. '
                                    'Could be full name (__test_somecase) '
                                    'or short (somecase) '
                                    'mask is also possible via astrisks symbol __test_somecases_*')
        run_tests.add_argument("--verbose", "-v", type=int, default=0,
                               help='Prints more debug information')
        run_tests.add_argument("--silent", "-s", action='store_true',
                               help='Do not abort if tests have failed')
        run_tests.add_argument("--output-results", "-o", action='store_true',
                               help='Stores results as json')
        run_tests.add_argument("--old", action='store_true', help='In old versions of toncli tests had to have '
                                                                  'specific method_ids (starting from 0). If you '
                                                                  'still follow this convention, and want to run '
                                                                  'tests, provide this flag.')

    def set_updatelibs_parser(self):
        self.subparser.add_parser('update_libs')

    def set_func_parser(self):
        parser_func = self.subparser.add_parser('func', help=TextUtils.FUNC_HELP,
                                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                                description=textwrap.dedent(TextUtils.FUNC_HELP))
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
