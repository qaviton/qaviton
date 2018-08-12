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


#############################################################################
#                                                                           #
#                              Directories                                  #
#                                                                           #
#############################################################################


def get_root_directory():
    return os.path.dirname(os.path.abspath(__file__))


def get_project_directory(project_name):
    project_directory = os.path.realpath(__file__).split(project_name)
    if len(project_directory) > 2:
        raise Exception('project name {} appear more then once in the file path {}'.format(project_name, project_directory))
    return project_directory[0] + project_name


def get_report_directory(project_name):
    return get_project_directory(project_name) + s + 'reports'


def create_directory(directory_path):
    if not os.path.exists(os.path.dirname(directory_path)):
        try:
            os.makedirs(os.path.dirname(directory_path))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def get_subdirectories(directory_path):
    for i in os.walk(directory_path):
        results = []
        for subdir_name in i[1]:
            results.append(directory_path + s + subdir_name)
        return results


def get_subdirectories_deep(directory_path):
    return [x[0] for x in os.walk(directory_path)]


def get_repository(root_directory, repository_name):
    """
    this function will get the neighboring repository relative
    to your root directory with the same parent directory
    example:
        parent_dir:
            root_dir
            repo_dir
    :param root_directory: str
    :param repository_name: str
    :return:
    """
    if root_directory[-1] == s:
        root_directory = root_directory[:-1]
    return root_directory.rsplit(s, 1)[0] + s + repository_name + s


def clean_directory(root_directory, pattern):
    files = deep_files_search(root_directory, '*' + pattern)
    for file in files:
        if pattern in str(file):
            if os.path.isfile(file):
                os.unlink(file)


def delete_directory_contents(root_directory):
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








