# Copyright (c) 2022 Disintar LLP Licensed under the Apache License Version 2.0

import argparse
import sys
import textwrap
import configparser
import os

from toncli.modules.utils.commands.commands_executer import CommandsExecuter
from toncli.modules.utils.parsers.parser_utils import ParserUtil
from toncli.modules.utils.system.conf import config_file
from toncli.modules.utils.system.log import logger
from toncli.modules.utils.check_hash import check_2_libs_actual, get_libs_paths
from toncli.modules.utils.text.text_utils import TextUtils

def main():
    '''
    CLI interface definition
    :return:
    '''
    
    # Enabling coloured text in Windows terminals
    os.system("")
    
    # This is concept of nft https://disintar.io
    # Nft information parse will be added in next versions of CLI
    # print("disintar.io NFT owners today say: 🙈 🙉 🙊")

    # TODO: add logging verbose
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(TextUtils.HELP_TEXT))
    parser.add_argument("-v", "--version", help="package version", action='store_true')

    config = configparser.ConfigParser()
    config.read(config_file)
    config_default = config['DEFAULT']
    warn = config_default.get('LIBS_WARNING') != 'False'
    if warn:
        if not check_2_libs_actual():
            local_lib_path, global_lib_path = get_libs_paths()
            logger.warning(
                TextUtils.VERSION_WARNING,
                global_lib_path,
                local_lib_path
            )
    
    parserUtil = ParserUtil(parser)
    parserUtil.set_all_parsers()

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
