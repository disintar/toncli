import sys
from toncli.modules.utils.fift.cli_lib import process_build_cli_lib_command

class BuildCliLibsCommand():
    def __init__(self):
        process_build_cli_lib_command(sys.argv[2:])
        