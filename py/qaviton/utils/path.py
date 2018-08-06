import os


def get(file):
    """Returns abs path relative to this file and not cwd
        eample:
            from qaviton.utils import path

            path.get(__file__)('../../path/to/file.txt')
    """
    return lambda p: os.path.abspath(os.path.join(os.path.dirname(file), p))
