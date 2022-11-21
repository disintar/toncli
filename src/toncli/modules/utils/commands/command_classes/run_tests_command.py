from argparse import ArgumentParser
import sys
from toncli.modules.utils.test.tests import TestsRunner
from toncli.modules.utils.system.argparse_fix import argv_fix


class RunTestsCommand():
    def __init__(self, string_kwargs, parser: ArgumentParser):
        # Meh
        real_argv, kwargs = argv_fix(sys.argv, string_kwargs)
        args = parser.parse_args(['run_tests', *kwargs])

        test_runner = TestsRunner()

        test_runner.run(args.contracts.split() if args.contracts else None,
                        tests=real_argv[2:],
                        verbose=args.verbose,
                        output_results=args.output_results,
                        run_tests_old_way=args.old,
                        silent=args.silent)
