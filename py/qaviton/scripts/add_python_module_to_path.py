"""
use this script to add your module to the python path.
this way tou can run your module/package locally from anywhere

example_1:
    description:
        put the script in the directory you want to add
        to the path and run the script.

    shell commands:
        python add_python_module_to_path.py

example_2:
    description:
        call the script and use the module_path
        parameter to point it to the module path

    shell commands:
        python add_python_module_to_path.py module_path /path/to/module/directory
"""
import os
import sys
from distutils.sysconfig import get_python_lib


if os.name == 'nt':
    s = '\\'
else:
    s = '/'


def get_external_arguments():
    args = sys.argv
    module_path = None
    if len(args) > 2:
        for i in range(1, len(args)):
            if args[i] == 'module_path':
                if len(args) > i + 1:
                    module_path = args[i+1]
    return module_path


def get_module_default_path():
    return os.path.dirname(os.path.abspath(__file__))


def get_project_name(module_directory):
    return module_directory.split(s)[-1]


def create_new_site_package(project_name, module_directory):
    path = '{}{}{}.pth'.format(get_python_lib(), s, project_name)
    if not os.path.exists(path):
        path_file = open(path, 'w')
        path_file.write(module_directory)
        path_file.close()
    else:
        raise Exception("path file: {} exist".format(path))


def add_module_to_site_packages(module_path=None):
    if module_path is None:
        module_path = get_module_default_path()
    project_name = get_project_name(module_path)
    create_new_site_package(project_name, module_path)


if __name__ == "__main__":
    add_module_to_site_packages(get_external_arguments())
