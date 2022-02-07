import configparser
import os
import shutil

from appdirs import user_config_dir
from colorama import Fore, Style

from tncli.modules.utils.system.check_executable import safe_get_version, check_executable
from tncli.modules.utils.system.log import logger

gr = Fore.GREEN
bl = Fore.CYAN
rs = Style.RESET_ALL

project_root = os.path.realpath(__file__)
project_root = "/".join(project_root.split("/")[:-4])  # get root folder of tncli/src

# Folder to store config files in
config_folder = user_config_dir('tncli')

# Create if not exist
if not os.path.exists(config_folder):
    config = configparser.ConfigParser()
    config.read(f'{project_root}/config.ini')

    config['executable'] = {
        'func': '',
        'fift': '',
        'lite-client': '',
    }

    logger.info(f"🥰 {gr}First time run{rs} - i'll create config folder 4you and save some stuff there")
    logger.info(f"🤖 Check all executables are installed...")

    # Here we need to correctly define executable path
    new_executable, is_executable_changes = check_executable(dict(config['executable']))
    config['executable'] = new_executable

    logger.info(f"🥰 Feel free to change it if needed: {bl}{config_folder}/config.ini{rs}")

    os.makedirs(config_folder)

    with open(f'{config_folder}/config.ini', 'w') as config_file:
        config.write(config_file)

    shutil.copytree(f"{project_root}/lib/", f"{config_folder}",
                    dirs_exist_ok=True)  # copy all fift / func libs

config_file = f"{config_folder}/config.ini"

config = configparser.ConfigParser()
config.read(config_file)

if 'toncenter_mainnet' not in config['DEFAULT'] or 'toncenter_testnet' not in config['DEFAULT']:
    config['DEFAULT']['toncenter_mainnet'] = 'https://toncenter.com/api/v2'
    config['DEFAULT']['toncenter_testnet'] = 'https://testnet.toncenter.com/api/v2'

    with open(config_file, 'w') as config_f:
        config.write(config_f)

main_config = config['DEFAULT']

# URI to get config from
config_uri = {
    'testnet': main_config.get('testnet'),
    'mainnet': main_config.get('mainnet')
}

toncenter = {
    'mainnet': main_config.get('toncenter_mainnet'),
    'testnet': main_config.get('toncenter_testnet'),
}

# Here we need to correctly define executable path
new_executable, is_executable_changes = check_executable(dict(config['executable']))

if is_executable_changes:
    config['executable'] = new_executable

    with open(f'{config_folder}/config.ini', 'w') as config_file:
        config.write(config_file)

executable = {
    'fift': new_executable['fift'],
    'func': new_executable['func'],
    'lite-client': new_executable['lite-client'],
}
