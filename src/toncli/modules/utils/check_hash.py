import glob
import hashlib
import os
import pathlib

from appdirs import user_config_dir

from toncli.modules.utils.system.conf import project_root


def get_dir_hashes(path):
    ans = []
    for path, subdirs, files in os.walk(path):
        for name in list(sorted(files)):
            fname = os.path.join(path, name)
            with open(fname, 'rb') as file:
                data = file.read()
                ans.append(hashlib.md5(data).hexdigest())
    return ans


def check_2_libs_actual():
    global_path, local_path = get_libs_paths()

    global_fift_hashes = get_dir_hashes(os.path.abspath(f"{global_path}/fift-libs"))
    local_fift_hashes = get_dir_hashes(os.path.abspath(f"{local_path}/fift-libs"))

    global_func_hashes = get_dir_hashes(os.path.abspath(f"{global_path}/func-libs"))
    local_func_hashes = get_dir_hashes(os.path.abspath(f"{local_path}/func-libs"))

    return global_fift_hashes == local_fift_hashes and global_func_hashes == local_func_hashes


def get_libs_paths():
    return os.path.abspath(f"{project_root}/lib"), user_config_dir('toncli')
