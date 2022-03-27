import sys
import tempfile
from typing import List, Optional, Dict, Any

from jinja2 import Environment, select_autoescape, FileSystemLoader

from toncli.modules.utils.system.conf import project_root
from toncli.modules.utils.fift.fift import Fift
from toncli.modules.utils.system.log import logger


def build_cli_lib(to_save_location: Optional[str] = None, render_kwargs: Optional[Dict[str, Any]] = None) -> str:
    """Create project-specific cli.fif lib"""

    if not to_save_location:
        to_save_location: str = tempfile.mkstemp(suffix='.fif')[1]
        logger.info(f"👽 Save ton-cli to {to_save_location}")

    loader = FileSystemLoader(f"{project_root}/modules/fift")

    env = Environment(
        loader=loader,
        autoescape=select_autoescape()
    )

    template = env.get_template(f"cli.fif.template")

    render_kwargs = {} if render_kwargs is None else render_kwargs

    if 'is_project' not in render_kwargs:
        render_kwargs['is_project'] = 0

    rendered = template.render(**render_kwargs)

    with open(to_save_location, 'w', encoding='utf-8') as f:
        f.write(rendered)

    return to_save_location


def process_build_cli_lib_command(args: List[str]):
    """Process toncli build-cli-lib"""

    script_path = build_cli_lib(args[0] if len(args) else None, {'project_root': ''})

    fift = Fift('run', args=[script_path])
    fift.run()

    sys.exit(0)


if __name__ == "__main__":
    build_cli_lib('lol')
