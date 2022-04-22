from argparse import ArgumentParser
import sys
from toncli.modules.tests.tests import TestsRunner
from toncli.modules.utils.system.argparse_fix import argv_fix

class RunTestsCommand():
    def __init__(self, string_kwargs, parser: ArgumentParser):
        _, kwargs = argv_fix(sys.argv, string_kwargs)
        args = parser.parse_args(['run_tests', *kwargs])

        test_runner = TestsRunner()
        test_runner.run(args.contracts.split() if args.contracts else None,
                        verbose=args.verbose,
                        output_results=args.output_results)
