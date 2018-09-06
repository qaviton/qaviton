from qaviton.utils.log_handler import get_logger, log_levels


def testlogger():
    log1 = get_logger('log1.txt', log_name='log1')
    log1.debug('debug msg')
    log1.info('info msg')
    log1.warning('warning msg')
    log1.error('error msg')
    log1.critical('critical msg')

    log2 = get_logger('log2.txt', log_name='log2', log_level=log_levels.INFO, log_to_console=False)
    log2.debug('debug msg')
    log2.info('info msg')
    log2.warning('warning msg')
    log2.error('error msg')
    log2.critical('critical msg')
