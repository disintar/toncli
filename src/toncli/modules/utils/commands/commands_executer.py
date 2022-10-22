# Copyright (c) 2022 Disintar LLP Licensed under the Apache License Version 2.0

import sys
from toncli.modules.utils.commands.command_classes.help_or_h_command import HelpOrHCommand
from toncli.modules.utils.commands.command_classes.lite_client_or_lc_command import LiteClientOrLcCommand
from toncli.modules.utils.system.argparse_fix import argv_fix
from toncli.modules.utils.system.log import logger
from argparse import ArgumentParser
from toncli.modules.utils.commands.command_classes.addrs_command import AddrsCommand
from toncli.modules.utils.commands.command_classes.build_cli_libs_command import BuildCliLibsCommand
from toncli.modules.utils.commands.command_classes.deploy_command import DeployCommand
from toncli.modules.utils.commands.command_classes.func_or_fc_or_build_command import FuncOrFcOrBuildCommand
from toncli.modules.utils.commands.command_classes.get_command import GetCommand
from toncli.modules.utils.commands.command_classes.local_version_command import LocalVersionCommand
from toncli.modules.utils.commands.command_classes.run_or_fift_or_f_command import RunOrFiftOrFCommand
from toncli.modules.utils.commands.command_classes.run_tests_command import RunTestsCommand
from toncli.modules.utils.commands.command_classes.run_transaction_command import RunTransactionCommand
from toncli.modules.utils.commands.command_classes.send_boc_command import SendBocCommand
from toncli.modules.utils.commands.command_classes.send_command import SendCommand
from toncli.modules.utils.commands.command_classes.start_command import StartCommand
from toncli.modules.utils.commands.command_classes.to_integer_command import ToIntegerCommand
from toncli.modules.utils.commands.command_classes.update_libs_command import UpdateLibsCommand
from toncli.modules.utils.commands.command_classes.wallet_command import WalletCommand


class CommandsExecuter():
    command = ""
    string_kwargs = []
    parser: ArgumentParser

    def __init__(self, command, string_kwargs, parser):
        _, kwargs = argv_fix(sys.argv, string_kwargs)

        if len(kwargs) == 0 and not command:
            parser.print_help()
            sys.exit(0)

        self.command = command
        self.string_kwargs = string_kwargs
        self.parser = parser
        if command in self.command_mapper:
            self.command_mapper[command](self)
        else:
            logger.error("🔎 Can't find such command")
            sys.exit()

    # define the function blocks
    def addrs_command(self):
        return AddrsCommand()

    def run_tests_command(self):
        return RunTestsCommand(self.string_kwargs, self.parser)

    def send_boc_command(self):
        return SendBocCommand(self.string_kwargs, self.parser)

    def send_command(self):
        return SendCommand(self.string_kwargs, self.parser)

    def wallet_command(self):
        return WalletCommand()

    def update_libs(self):
        return UpdateLibsCommand()

    def run_transaction(self):
        return RunTransactionCommand(self.parser)

    def get_command(self):
        return GetCommand(self.string_kwargs, self.parser)

    def deploy_command(self):
        return DeployCommand(self.string_kwargs, self.parser)

    def start_command(self):
        return StartCommand(self.parser)

    def tointeger_command(self):
        return ToIntegerCommand(self.string_kwargs)

    def func_or_fc_or_build_command(self):
        return FuncOrFcOrBuildCommand(self.command, self.string_kwargs, self.parser)

    def lite_client_or_lc_command(self):
        return LiteClientOrLcCommand(self.string_kwargs, self.parser)

    def run_or_fift_or_f_command(self):
        return RunOrFiftOrFCommand(self.command, self.string_kwargs, self.parser)

    def build_cli_libs_command(self):
        return BuildCliLibsCommand()

    def local_version_command(self):
        return LocalVersionCommand()

    def help_or_h_command(self):
        return HelpOrHCommand(self.parser)

    command_mapper = {
        "-h": help_or_h_command,
        "--help": help_or_h_command,
        "-v": local_version_command,
        "--version": local_version_command,
        "build_cli_libs": build_cli_libs_command,
        "run": run_or_fift_or_f_command,
        "fift": run_or_fift_or_f_command,
        "f": run_or_fift_or_f_command,
        "lite-client": lite_client_or_lc_command,
        "lc": lite_client_or_lc_command,
        "func": func_or_fc_or_build_command,
        "fc": func_or_fc_or_build_command,
        "build": func_or_fc_or_build_command,
        "tointeger": tointeger_command,
        "addrs": addrs_command,
        "start": start_command,
        "run_tests": run_tests_command,
        "sendboc": send_boc_command,
        "send": send_command,
        "get": get_command,
        "deploy": deploy_command,
        "wallet": wallet_command,
        "update_libs": update_libs,
        "run_transaction": run_transaction
    }
