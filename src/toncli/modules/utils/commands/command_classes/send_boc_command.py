from argparse import ArgumentParser
import sys
from toncli.modules.utils.fift.fift import Fift
from toncli.modules.utils.lite_client.lite_client import LiteClient
from toncli.modules.utils.system.argparse_fix import argv_fix
from toncli.modules.utils.system.log import logger

class SendBocCommand():
    def __init__(self, string_kwargs, parser: ArgumentParser):
        real_args, kwargs = argv_fix(sys.argv, string_kwargs)
        args = parser.parse_args(['func', *kwargs])
        # Parse kwargs by argparse
        kwargs = dict(args._get_kwargs())

        file = kwargs['file']
        ext = file.name.split('.')[-1]
        if ext == 'boc':
            lc = LiteClient(command="sendfile", args=[file.name],
                        kwargs={'net': kwargs['net'], 'update': False, 'lite_client_args': '-v 1'})
            lc.run()
        elif ext == 'fif':
            fift_params = real_args[2:]
            fift = Fift(command='sendboc', args=fift_params)
            fift.run()
        else:
            logger.error('This file extension is not supported. Supported extensions are .boc and .fif')
