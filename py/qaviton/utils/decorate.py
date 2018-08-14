# TODO: refactor
from time import time


retries = 1


def generic_method_executioner(self, method, retries, *args, **kw):
    """this function can only be used on objects with methods and a log object"""
    t = time()
    tries = retries + 1
    for Try in range(tries):
        try:
            results = method(self, *args, **kw)
            break
        except Exception as error:
            caller = self.__class__.__name__ + '.' + method.__name__
            self.log.debug('{} arguments: {}{}'.format(caller, args, kw))
            self.log.debug('exception raised: handler method is to retry')
            self.log.debug('retries left {}'.format(retries - Try))
            if Try == retries:
                self.log.exception(error)
                raise Exception(error)
            else:
                self.log.error(error)
    t = time() - t
    return t, results


def dont_log(*args, **kw):
    """DecoratorConfig self.decorator_log can be configured to use this if no log is required"""
    pass


def log_info(self, method, t, *args, **kw):
    """this function can only be used on objects with methods and a log object"""
    msg = '{}: {} {}'.format('[%2.4f sec]' % t, self.__class__.__name__, method.__name__)
    self.log.info(msg)


def log_debug(self, method, t, *args, **kw):
    """this function can only be used on objects with methods and a log object"""
    msg = '{}: {} {} arguments {}{}'.format('[%2.4f sec]' % t, self.__class__.__name__, method.__name__, args, kw)
    self.log.debug(msg)


# def generic_decorator(retries=retries):
#     """this function can only be used on objects with methods and a log object"""
#     def decorator(method):
#         def wrapper(self, *args, **kw):
#             t, results = generic_method_executioner(self, method, retries, *args, **kw)
#             generic_log(self, method, t, *args, **kw)
#             return results
#         return wrapper
#     return decorator


class DecoratorConfig(object):
    """this class is meant to create a configurable decorator for objects methods with a self.log"""

    def __init__(self, retries=retries, decorator_log=log_info):
        self.retries = retries
        self.decorator_log = decorator_log

    def get_params(self, retries=None, decorator_log=None):
        if retries is None:
            retries = self.retries
        if decorator_log is None:
            decorator_log = self.decorator_log
        return retries, decorator_log

    def generic_decorator(self, retries=None, decorator_log=None):
        """
        this function can only be used on objects with methods and a log object
        :param retries: int the number of retries
        :param decorator_log: choose a log formatter function, default is log_info
        :return:
        """
        def decorator(method):
            def wrapper(obj, *args, **kw):
                retries_param, decorator_log_param = self.get_params(retries, decorator_log)
                t, results = generic_method_executioner(obj, method, retries_param, *args, **kw)
                decorator_log_param(obj, method, t, *args, **kw)
                return results
            return wrapper
        return decorator


if __name__ == "__main__":

    from qaviton.core.core.ui.test_model import create_logger, log_file
    log = create_logger(log_file)

    decorator_obj = DecoratorConfig(retries=2, decorator_log=log_debug)
    decorator = decorator_obj.generic_decorator

    class A:
        def __init__(self):
            self.log = log

        @decorator()
        def b(self, name):
            print(name)

    a = A()
    a.b('shalomm')

    # import functools
    #
    # class MyDecorator(object):
    #     def __init__(self, argument):
    #         self.arg = argument
    #
    #     def __call__(self, fn):
    #         @functools.wraps(fn)
    #         def decorated(*args, **kwargs):
    #             print "In my decorator before call, with arg %s" % self.arg
    #             fn(*args, **kwargs)
    #             print "In my decorator after call, with arg %s" % self.arg
    #         return decorated
    #
    # @MyDecorator(3)
    # def some1(a):
    #     print(a)
    #
    # some1(5)
