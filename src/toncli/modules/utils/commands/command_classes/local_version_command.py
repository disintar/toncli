from colorama import Fore, Style
import pkg_resources
import requests
from toncli.modules.utils.system.log import logger

gr = Fore.GREEN
bl = Fore.CYAN
rs = Style.RESET_ALL

class LocalVersionCommand():
    def __init__(self):
        update_text = f'''\n🦋 New {bl}TONCLI{rs} version is available. Please install it using "{bl}pip install --upgrade toncli{rs}".\n 
You should also update your binaries for this version. Please download the binaries depending on your system at the links provided. \n 
    Windows : {bl}https://github.com/SpyCheese/ton/actions/runs/2589030151{rs} \n 
    Linux : {bl}https://github.com/SpyCheese/ton/actions/runs/2585669126{rs} \n 
    MacOs : {bl}https://github.com/SpyCheese/ton/actions/runs/2585669126{rs} \n'''

        version_local = pkg_resources.get_distribution("toncli").version
        try:
            version_global = requests.get('https://pypi.org/pypi/toncli/json').json()['info']['version']
            if version_global and version_global != version_local:
                logger.info(update_text)
        except BaseException:
            pass

        logger.info(f'v{version_local}')
