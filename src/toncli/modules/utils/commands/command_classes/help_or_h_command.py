import sys
from toncli.modules.utils.fift.cli_lib import process_build_cli_lib_command

class HelpOrHCommand():
    def __init__(self, parser):
        parser.print_help()
        sys.exit(0)
        