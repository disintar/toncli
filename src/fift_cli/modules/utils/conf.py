import configparser
import os

from appdirs import user_config_dir

project_root = os.path.realpath(__file__)
project_root = "/".join(project_root.split("/")[:-4])  # get root folder of fift-cli/src

config = configparser.ConfigParser()
config.read(f'{project_root}/fift_cli/config.ini')

main_config = config['DEFAULT']

# URI to get config from
config_uri = {
    'testnet': main_config.get('testnet'),
    'mainnet': main_config.get('mainnet')
}

# Folder to store config files in
config_folder = user_config_dir('fift_cli')

if 'config_folder' in main_config:
    config_folder = main_config['config_folder']

# Create if not exist
if not os.path.exists(config_folder):
    os.makedirs(config_folder)
