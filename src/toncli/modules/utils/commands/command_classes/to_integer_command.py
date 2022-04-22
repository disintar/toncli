import sys
from toncli.modules.utils.system.argparse_fix import argv_fix
from toncli.modules.utils.system.log import logger

class ToIntegerCommand():
    def __init__(self, string_kwargs):
        args, _ = argv_fix(sys.argv, string_kwargs)
        string_to_encode = " ".join(args[2:])
        logger.info(f"👻  Your string: {int(string_to_encode.encode().hex(), 16)}")
        sys.exit()
            