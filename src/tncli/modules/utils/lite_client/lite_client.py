import shlex
import subprocess
import sys
from typing import Optional, List
from tncli.modules.utils.system.log import logger
from tncli.modules.utils.lite_client.commands import lite_client_execute_command


class LiteClient:
    def __init__(self, command: str, args: Optional[List[str]] = None, kwargs: Optional[dict] = None,
                 get_output: bool = False):
        self.command = command
        self.get_output = get_output

        if kwargs:
            self.kwargs = kwargs
            self.kwargs['lite_client_args'] = shlex.split(self.kwargs['lite_client_args'])
        else:
            self.kwargs = {'lite_client_args': [],
                           'net': 'testnet',
                           'update': False}

        self.args = args

    def run(self) -> Optional[bytes]:
        if not self.command or self.command == 'interactive':
            self.run_interactive()
        elif self.command:
            return self.run_command()
        else:
            logger.error("🔎 Can't find such command")
            sys.exit()

    def run_interactive(self):
        command = lite_client_execute_command(self.kwargs['net'], self.kwargs['lite_client_args'],
                                              self.kwargs['update'])
        subprocess.run(command)

    def run_command(self) -> Optional[bytes]:
        command = lite_client_execute_command(self.kwargs['net'],
                                              [*self.kwargs['lite_client_args'], '-c',
                                               " ".join([self.command, *self.args])],
                                              self.kwargs['update'])
        if not self.get_output:
            subprocess.run(command)
        else:
            output = subprocess.check_output(command)
            return output

    def run_safe(self):
        output = self.run()

        if output:
            output = output.decode()

        if not output or 'result' not in output:
            logger.error("👻 There is a problem when trying to run get method of contract")
            logger.error("".join(output if output else "No output"))
            sys.exit()

        return output
