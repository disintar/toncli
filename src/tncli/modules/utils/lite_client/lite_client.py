import os
import shlex
import subprocess
import sys
from typing import Optional, List
from tncli.modules.utils.system.log import logger
from tncli.modules.utils.lite_client.commands import lite_client_execute_command


class LiteClient:
    def __init__(self, command: str, args: Optional[List[str]] = None, kwargs: Optional[dict] = None):
        print(command, args, kwargs)

        self.command = command

        if kwargs:
            self.kwargs = kwargs
            self.kwargs['lite_client_args'] = shlex.split(self.kwargs['lite_client_args'])
        else:
            self.kwargs = {'lite_client_args': [],
                           'net': 'testnet',
                           'update': False}

        self.args = args

    def run(self):
        if not self.command or self.command == 'interactive':
            self.run_interactive()
        elif self.command:
            self.run_command()
        else:
            logger.error("🔎 Can't find such command")
            sys.exit()

    def run_interactive(self):
        command = lite_client_execute_command(self.kwargs['net'], self.kwargs['lite_client_args'],
                                              self.kwargs['update'])
        subprocess.run(command)

    def run_command(self):
        command = lite_client_execute_command(self.kwargs['net'],
                                              [*self.kwargs['lite_client_args'], '-c', " ".join([self.command, *self.args])],
                                              self.kwargs['update'])
        print(command)
        subprocess.run(command)
