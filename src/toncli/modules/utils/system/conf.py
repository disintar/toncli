# Copyright (c) 2022 Disintar LLP Licensed under the Apache License Version 2.0

import configparser
import os
import platform
import re
import shutil
import tempfile

from appdirs import user_config_dir
from colorama import Fore, Style
from copy import deepcopy
from toncli.modules.utils.system.check_executable import safe_get_version, check_executable
from toncli.modules.utils.system.log import logger

gr = Fore.GREEN
bl = Fore.CYAN
rs = Style.RESET_ALL

project_root = os.path.realpath(__file__)

project_root = os.path.abspath(os.path.sep.join(project_root.split(os.path.sep)[:-4]))  # get root folder of toncli/src

# Folder to store config files in
config_folder = user_config_dir('toncli')

name_replace = ['', '']

# fix win encoding
# todo: find normal fix
if platform.system() == 'Windows':
    old_user = os.getlogin()  # Old cyrillic name
    has_cyrillic = bool(re.search('[а-яА-Я]', old_user))
    user = config_folder.split(os.path.sep)[2]  # New name (in tempfile it's encoded)
    project_root = project_root.replace(old_user, user)  # New path with encoded cyrillic name of user
    if has_cyrillic:
        name_replace = [old_user, user]


def getcwd():
    path = os.getcwd()

    # fix win cyrillic
    if platform.system() == 'Windows':
        path = path.replace(name_replace[0], name_replace[1])

    return path


def get_subdirs(path: str) -> list:
    return [sub_dir.name for sub_dir in os.scandir(path) if sub_dir.is_dir()]


def get_projects() -> list:
    project_loc = os.path.join(project_root, "projects")
    return get_subdirs(project_loc)


# Create if not exist
if not os.path.exists(os.path.abspath(f"{config_folder}/config.ini")):
    config = configparser.ConfigParser()
    config.read(os.path.abspath(f'{project_root}/config.ini'))

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

    with open(os.path.abspath(f'{config_folder}/config.ini'), 'w') as config_file:
        config.write(config_file)

    shutil.copytree(os.path.abspath(f"{project_root}/lib/"), os.path.abspath(f"{config_folder}"),
                    dirs_exist_ok=True)  # copy all fift / func libs

config_file = os.path.abspath(f"{config_folder}/config.ini")

config = configparser.ConfigParser()
config.read(os.path.abspath(f"{config_folder}/config.ini"))

if 'toncenter_mainnet' not in config['DEFAULT'] or 'toncenter_testnet' not in config['DEFAULT']:
    config['DEFAULT']['toncenter_mainnet'] = 'https://toncenter.com/api/v2'
    config['DEFAULT']['toncenter_testnet'] = 'https://testnet.toncenter.com/api/v2'

    with open(config_file, 'w') as config_f:
        config.write(config_f)

main_config = config['DEFAULT']

# URI to get config from
config_uri = {
    'testnet': main_config.get('testnet'),
    'mainnet': main_config.get('mainnet'),
    'ownnet': main_config.get('ownnet', ''),
}

toncenter = {
    'mainnet': main_config.get('toncenter_mainnet'),
    'testnet': main_config.get('toncenter_testnet'),
    'ownnet': main_config.get('toncenter_ownnet', ''),
}

# Here we need to correctly define executable path
new_executable, is_executable_changes = check_executable(dict(config['executable']))

if is_executable_changes:
    config['executable'] = new_executable

    with open(os.path.abspath(f'{config_folder}/config.ini'), 'w') as cfg_path:
        config.write(cfg_path)

executable = {
    'fift': new_executable['fift'],
    'func': new_executable['func'],
    'lite-client': new_executable['lite-client'],
}

lite_client_tries = 7
