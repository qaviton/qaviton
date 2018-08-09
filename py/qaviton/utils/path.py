import os


def of(__file__):
    """Returns abs path relative to this file and not cwd
        example:
            from qaviton.utils import path

            path.of(__file__)('../../path/to/file.txt')
    """
    return lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
