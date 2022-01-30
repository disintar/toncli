import subprocess
from typing import Optional, List


def run(command: List[str]) -> Optional[str]:
    """Run command and return output"""
    get_output = subprocess.check_output(command)

    if get_output:
        return get_output.decode()
