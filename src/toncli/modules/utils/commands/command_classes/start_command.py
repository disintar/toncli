from argparse import ArgumentParser
from toncli.modules.projects import ProjectBootstrapper

class StartCommand():
    def __init__(self, parser: ArgumentParser):
        args = parser.parse_args()
        # if folder name not defined just take project name
        folder_name = args.name if args.name else args.project
        bootstrapper = ProjectBootstrapper(project_name=args.project, folder_name=folder_name)
        bootstrapper.deploy()
            