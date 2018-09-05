import errno
import ntpath
import os
import pathlib
import shutil
import zipfile
from fnmatch import fnmatch, filter
from io import BytesIO
import imageio
from qaviton.utils.operating_system import s
import yaml
import glob


#############################################################################
#                                                                           #
#                              Directories                                  #
#                                                                           #
#############################################################################


def find_replace(directory, find, replace, pattern):
    """replace file patterns
    search for files with certain name patterns
    and find & replace a pattern inside the files"""
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in filter(files, pattern):
            filepath = os.path.join(path, filename)
            with open(filepath) as f:
                s = f.read()
            s = s.replace(find, replace)
            with open(filepath, "w") as f:
                f.write(s)


def copy_directory(src, dest):
    "dest should be a directory path that does not exist"
    try:
        shutil.copytree(src, dest)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            raise Exception('Directory not copied') from e


def get_directory_from_file(__file__: str):
    return os.path.dirname(os.path.abspath(__file__))


def create_directory(directory_path: str):
    if not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path, exist_ok=True)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
        except Exception as e:
            if not os.path.exists(directory_path):
                raise e


def create_directory_from_file(file_path: str):
    if not os.path.exists(file_path):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
        except Exception as e:
            if not os.path.exists(os.path.dirname(file_path)):
                raise e


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
    """delete directory and all its contents

    if this does not work because of permission error consider using:
        windows: filer.os.system('rd /s /q {}'.format(root_directory))
        linux/mac: filer.os.system('rm -rf {}'.format(root_directory))

        example:
            delete_directory_contents(test_report_directory_path)
    """
    for the_file in os.listdir(root_directory):
        file_path = os.path.join(root_directory, the_file)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def delete_directory(directory):
    """delete directory and all its contents
    preferably use delete_directory_contents function instead
    """
    if s == '\\':
        os.system('rd /s /q {}'.format(directory))
    else:
        os.system('rm -rf {}'.format(directory))
    if os.path.exists(directory):
        raise Exception("directory could not be deleted")


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


def get_dir_files(dir_path):
    return [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]


def rename_file(name, new_name):
    os.rename(name, new_name)


def delete_file(name):
    os.remove(name)


def delete_all_files(dir):
    files = glob.glob(dir + s + '*')
    for f in files:
        os.remove(f)


def get_file_full_name(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def get_file_name_and_type(file_full_name):
    return file_full_name.split('.')


def create_file(file_path: str):
    try:
        open(file_path, 'w+').close()
    except Exception as e:
        if not os.path.exists(file_path):
            raise e


def get_file_name(file_path):
    return os.path.basename(file_path)


def get_file_directory(path):
    return os.path.dirname(os.path.realpath(path))


def copy_file(src_file, dest_file):
    """use this in cases where another program
    might try to copy to same dest_file
    """
    if not os.path.exists(dest_file):
        try:
            shutil.copyfile(src_file, dest_file)
        except Exception as e:
            if not os.path.exists(dest_file):
                raise e


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