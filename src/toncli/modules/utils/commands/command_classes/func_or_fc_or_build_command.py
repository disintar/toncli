from argparse import ArgumentParser
import sys
from toncli.modules.utils.func.func import Func
from toncli.modules.utils.system.argparse_fix import argv_fix

class FuncOrFcOrBuildCommand():
    def __init__(self, command, string_kwargs, parser: ArgumentParser):
        real_args, kwargs = argv_fix(sys.argv, string_kwargs)
        args = parser.parse_args(['func', *kwargs])

        # Parse kwargs by argparse
        kwargs = dict(args._get_kwargs())

        # Add support of toncli run ...
        if command != 'build':
            # Parse command (func [command])
            command = real_args[2] if len(real_args) > 2 else None
            args_to_pass = real_args[3:]
        else:
            args_to_pass = real_args[2:]

        # If use run command instead of f run - need to change start arg parse position

        func = Func(command, kwargs=kwargs, args=args_to_pass)
        func.run()
        