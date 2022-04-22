from argparse import ArgumentParser
import sys
from toncli.modules.utils.system.argparse_fix import argv_fix
from toncli.modules.utils.fift.fift import Fift

class RunOrFiftOrFCommand():
    def __init__(self, command, string_kwargs, parser: ArgumentParser):
        if(len(sys.argv) >= 2):
            real_args, kwargs = argv_fix(sys.argv, string_kwargs)
            args = parser.parse_args(['fift', *kwargs])

            # Add support of toncli run ...
            if command != 'run':
                # Parse command (fift [command])
                command = real_args[2] if len(real_args) > 2 else None
                args_to_pass = real_args[3:]
            else:
                args_to_pass = real_args[2:]

            # Parse kwargs by argparse
            kwargs = dict(args._get_kwargs())

            # If use run command instead of f run - need to change start arg parse position
            fift = Fift(command, kwargs=kwargs, args=args_to_pass)
            fift.run()
            