import configparser
import os
import shutil

from appdirs import user_config_dir
from colorama import Fore, Style

from .log import logger

gr = Fore.GREEN
rs = Style.RESET_ALL

project_root = os.path.realpath(__file__)
project_root = "/".join(project_root.split("/")[:-4])  # get root folder of fift-cli/src

# Folder to store config files in
config_folder = user_config_dir('fift_cli')

# Create if not exist
if not os.path.exists(config_folder):
    config = configparser.ConfigParser()
    config.read(f'{project_root}/fift_cli/config.ini')

    config['executable'] = {
        'func': '',
        'fift': '',
        'lite-client': '',
    }

    logger.info(f"🥰 {gr}First time run{rs} - i'll create config folder 4you and save some stuff there")
    logger.info(f"🤖 Check all executables are installed...")

    for item in ['func', 'fift', 'lite-client']:
        executable_path = shutil.which(item)

        if executable_path:
            config['executable'][item] = executable_path
        else:
            logger.warning(f"🤖 Can't find executable for {item}, please specify it, e.g.: /usr/bin/{item}")
            config['executable'][item] = input("Path: ")

    logger.info(f"🥰 Feel free to change it if needed: {config_folder}/config.ini")

    os.makedirs(config_folder)

    with open(f'{config_folder}/config.ini', 'w') as config_file:
        config.write(config_file)

    shutil.copytree(f"{project_root}/lib/", f"{config_folder}",
                    dirs_exist_ok=True)  # copy all fift / func libs

config_file = f"{config_folder}/config.ini"

config = configparser.ConfigParser()
config.read(config_file)

main_config = config['DEFAULT']

# URI to get config from
config_uri = {
    'testnet': main_config.get('testnet'),
    'mainnet': main_config.get('mainnet')
}

executable_config = config['executable']

executable = {
    'fift': executable_config['fift'],
    'func': executable_config['func'],
    'lite-client': executable_config['lite-client'],
}
