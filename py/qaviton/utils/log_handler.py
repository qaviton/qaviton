import logging
from qaviton.utils.operating_system import s


format = '%(asctime)s:{%(levelname)s}:%(message)s'


class log_levels:
    CRITICAL = logging.CRITICAL
    FATAL = logging.FATAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    WARN = logging.WARN
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


def get_logger(
        log_file=None,
        log_level=log_levels.DEBUG,
        log_name=__name__,
        format=format,
        mode='w',
        log_to_console=True):

    # create logger
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)
    formatter = logging.Formatter(format)

    if log_to_console is True:
        # create console handler
        handler = logging.StreamHandler()
        # set handler log level
        handler.setLevel(log_level)
        # set handler formatter
        handler.setFormatter(formatter)
        # add handler to logger
        logger.addHandler(handler)

    if log_file is True:
        # create log_file handler
        handler = logging.FileHandler(log_file, mode)
        # set handler log level
        handler.setLevel(log_level)
        # set handler formatter
        handler.setFormatter(formatter)
        # add handler to logger
        logger.addHandler(handler)
    return logger


def get_file_paths_from_log(log):
    file_paths = []
    for handler in log.handlers:
        try:
            file_paths.append(handler.baseFilename)
        except:
            pass
    return file_paths


def get_log_file_directories(log):
    file_paths = get_file_paths_from_log(log)
    log_directory = []
    for file_path in file_paths:
        try:
            log_directory.append(file_path.rsplit(s, 1)[0] + s)
        except:
            pass
    return log_directory
