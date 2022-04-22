import sys
from toncli.modules.utils.transaction import run_transaction

class RunTransactionCommand():
    def __init__(self, parser):
        args = parser.parse_args()
        run_transaction(args.net,
                        args.smc_address,
                        args.logical_time,
                        args.transaction_hash,
                        args.function,
                        args.save)
        sys.exit()
