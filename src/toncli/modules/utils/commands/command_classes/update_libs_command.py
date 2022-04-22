import os
import shutil
from toncli.modules.utils.check_hash import get_libs_paths
from toncli.modules.utils.system.log import logger

class UpdateLibsCommand():
    def __init__(self):
        global_lib_path, local_lib_path = get_libs_paths()
        folder_names = ["fift-libs", "func-libs", "test-libs" ]
        for folder_name in folder_names:
            shutil.copytree(os.path.abspath(f"{global_lib_path}/{folder_name}"), os.path.abspath(f"{local_lib_path}/{folder_name}"),
                            dirs_exist_ok=True)

        logger.info("Succesfully copied %s\nfrom %s\nto %s",
                                ' '.join(folder_names),
                                    global_lib_path,
                                    local_lib_path)
