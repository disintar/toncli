import sys
from typing import List

from jinja2 import Environment, select_autoescape, FileSystemLoader

from tncli.modules.utils.conf import project_root
from tncli.modules.utils.log import logger


def build_cli_lib(to_save_location: str):
    """Create project-specific cli.fif lib"""
    loader = FileSystemLoader(f"{project_root}/tncli/modules/fift")

    env = Environment(
        loader=loader,
        autoescape=select_autoescape()
    )

    template = env.get_template(f"cli.fif.template")
    print(template)


def process_build_cli_lib_command(args: List[str]):
    """Process tncli build-cli-lib"""

    if not len(args):
        logger.error("🧛 You need to specify [build-to] argument")
        sys.exit(0)

    build_cli_lib(args[0])


if __name__ == "__main__":
    build_cli_lib('lol')
