from jsondiff import diff
from qaviton.exceptions import DiffException


def check_if_elements_are_identical(lst):
    return not lst or lst.count(lst[0]) == len(lst)


class asserts:
    """ assertions to compare values & find diffs """

    @staticmethod
    def elements_are_equal(*args):
        """ compare string value of 2+ variables, throw exception if expectation is not met """

        if check_if_elements_are_identical(args) is False:
            raise DiffException('values {} are not equal as expected'.format(args))

    @staticmethod
    def elements_are_not_equal(*args):
        """ compare string value of 2+ variables, throw exception if expectation is not met """

        if check_if_elements_are_identical(args) is True:
            raise DiffException('values {} are equal not as expected'.format(args))

    @staticmethod
    def value_is_in_a_list(lst, value):
        if value not in lst:
            raise DiffException("value {} doesn't exist in the list".format(value))

    @staticmethod
    def there_is_no_diff(var1, var2):
        diffs = diff(var1, var2)
        if type(diffs) is dict:
            if len(diffs) > 0:
                raise DiffException('found unexpected diffs {}'.format(diffs))

    @staticmethod
    def there_is_a_diff(var1, var2):
        diffs = diff(var1, var2)
        if type(diffs) is dict:
            if len(diffs) == 0:
                raise DiffException('expected diffs {} not found'.format(diffs))
