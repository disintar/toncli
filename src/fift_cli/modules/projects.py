import os
import shutil

from colorama import Fore, Style

from .log import logger


class ProjectBootstrapper:
    ''' Create new folder and copy files from src/projects/{project} to this folder'''

    def __init__(self, project_name: str, folder_name: str):
        self.project_name = project_name
        self.folder_name = folder_name

        self.project_location = os.path.realpath(__file__)  # current script path after pip install
        self.project_location = "/".join(self.project_location.split("/")[:-3])  # get root folder of fift-cli/src
        self.project_location = f"{self.project_location}/projects"

        self.current_location = os.getcwd()  # current location where we need to create folder with project

    def deploy(self):
        logger.info(f"🐒 I'll create folder {self.folder_name} with project {self.project_name} and all needed files")
        os.mkdir(self.folder_name)  # create new project dir

        shutil.copytree(f"{self.project_location}/{self.project_name}", f"{self.current_location}/{self.folder_name}",
                        dirs_exist_ok=True)  # copy all from default project to new directory

        logger.info(f"👑 Folder {Fore.GREEN}successfully {Style.RESET_ALL}created - happy blockchain hacking")
        logger.info(
            f"🐼 You now can do {Fore.GREEN}cd {self.folder_name} {Style.RESET_ALL}and {Fore.GREEN}fift-cli deploy -n testnet")
