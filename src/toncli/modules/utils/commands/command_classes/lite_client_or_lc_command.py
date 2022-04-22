from argparse import ArgumentParser
import sys
from toncli.modules.utils.lite_client.lite_client import LiteClient
from toncli.modules.utils.system.argparse_fix import argv_fix

class LiteClientOrLcCommand():
    def __init__(self, string_kwargs, parser: ArgumentParser):
        real_args, kwargs = argv_fix(sys.argv, string_kwargs)
        args = parser.parse_args(['lite-client', *kwargs])

        args_to_pass = real_args[3:]

        # Parse kwargs by argparse
        kwargs = dict(args._get_kwargs())

        # Parse command
        command = real_args[2] if len(real_args) > 2 else None

        # If use run command instead of f run - need to change start arg parse position
        lite_client = LiteClient(command, kwargs=kwargs, args=args_to_pass)
        lite_client.run()
        