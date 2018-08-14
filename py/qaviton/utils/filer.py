import errno
import ntpath
import os
import pathlib
import shutil
import zipfile
from fnmatch import fnmatch
from io import BytesIO
import imageio
from qaviton.utils.operating_system import s
import yaml


#############################################################################
#                                                                           #
#                              Directories                                  #
#                                                                           #
#############################################################################


def get_directory(__file__: str):
    return os.path.dirname(os.path.abspath(__file__))


def create_directory(directory_path: str):
    if not os.path.exists(os.path.dirname(directory_path)):
        try:
            os.makedirs(os.path.dirname(directory_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def get_subdirectories(directory_path: str):
    """ example:
    default_products_directory = settings.project_directory + 'products' + s
    default_products_directories = file_handler.get_subdirectories(default_products_directory)
    """
    for i in os.walk(directory_path):
        results = []
        for subdir_name in i[1]:
            results.append(directory_path + s + subdir_name)
        return results


def get_subdirectories_deep(directory_path: str):
    """get all subdirectories under root dir"""
    return [x[0] for x in os.walk(directory_path)]


def clean_directory(root_directory: str, pattern: str):
    """delete all files with the pattern under root dir"""
    files = deep_files_search(root_directory, '*' + pattern)
    for file in files:
        if pattern in str(file):
            if os.path.isfile(file):
                os.unlink(file)


def delete_directory_contents(root_directory: str):
    """ example:
    delete_directory_contents(test_report_directory_path)
    """
    for the_file in os.listdir(root_directory):
        file_path = os.path.join(root_directory, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

#############################################################################
#                                                                           #
#                                  Files                                    #
#                                                                           #
#############################################################################


def deep_files_search(root_directory, pattern="*.txt"):
    """
    search for files under a directory and all its subdirectories
    :param root_directory: /path/to/root/dir
    :param pattern: find_me.example
    :return: list of files paths
    """
    results = []
    for path, subdirs, files in os.walk(root_directory):
        for name in files:
            if fnmatch(name, pattern):
                results.append(str(pathlib.PurePath(path, name)))
    return results


def get_file_full_name(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def get_file_name_and_type(file_full_name):
    return file_full_name.split('.')


def create_file(file_path):
    create_directory(file_path)


def get_file_name(file_path):
    return os.path.basename(file_path)


def get_file_directory(path):
    return os.path.dirname(os.path.realpath(path))


#############################################################################
#                                                                           #
#                                 Images                                    #
#                                                                           #
#############################################################################


def create_gif(image_files, gif_file_path):
    """
    create gif from png files
    :param image_files: list of png file paths
            example:
                image_files = [
                    "/path/to/your/png/file1.png",
                    "/path/to/your/png/file2.png",
                    "/path/to/your/png/file3.png"
                ]
    :param gif_file_path: /path/to/your/gif/file.gif
    :return:
    """
    with imageio.get_writer(gif_file_path, mode='I') as writer:
        for file in image_files:
            image = imageio.imread(file)
            writer.append_data(image)


#############################################################################
#                                                                           #
#                                  ZIP                                      #
#                                                                           #
#############################################################################


def read_zipfile(zip_obj, name):
    """
    :param zip_obj: zip file object
    :param name: name of file inside the zip
            example:
                myzip.zip
                    'file.txt'
    :return:
    """
    with zip_obj.open(name) as f:
        return f.read()


def read_zipfiles(zip_obj):
    """
    :param zip_obj: zip file object
    :return:
    """
    zip_files = []
    for name in zip_obj.namelist():
        zip_files.append(read_zipfile(zip_obj, name))
    return zip_files


def open_zip(zip_path):
    return zipfile.ZipFile(zip_path)


def open_zip_from_inside_zip(zip_obj, zfile_name):
    zfiledata = BytesIO(zip_obj.read(zfile_name))
    return zipfile.ZipFile(zfiledata)


#############################################################################
#                                                                           #
#                                 YAML                                      #
#                                                                           #
#############################################################################

class parse:
    @staticmethod
    def yaml(file_path: str):
        with open(file_path) as y:
            return yaml.load(y.read())


class dump:
    @staticmethod
    def yaml(dump_to_file_path: str, parsed_yaml: dict):
        with open(dump_to_file_path, 'w') as y:
            y.write(yaml.dump(parsed_yaml, default_flow_style=False))