import sys
import inspect
import time


def timestamp():
    return str(int(time.time() * 1000))


def get_python_version():
    return sys.version_info


def funcname():
    return inspect.stack()[1][3]


def classname(frame=None):
    if frame is None:
        frame = inspect.stack()[1][0]
    args, _, _, value_dict = inspect.getargvalues(frame)
    # now lets check if the 1st parameter in the frame is named 'self'
    if len(args) and args[0] == 'self':
        # in that case self will be referenced in value_dict
        instance = value_dict.get('self', None)
        if instance:
            # return its class
            return getattr(instance, '__class__', None).__name__
    return None


class DynamicClass:
    """ do not touch this class!
        it is intended for dynamic objects
    """
    def __init__(self):
        pass


def list_to_object(keys, values):
    """
    create object in runtime.
    keys & values are lists/tuples with equal length
    :param keys: list
    :param values: list
    :return: dynamic_object
    """
    obj = DynamicClass()
    for i in range(len(keys)):
        setattr(obj, keys[i], values[i])
    return obj


def dict_to_object(dictionary):
    """
    parse a dictionary and return a dynamic object
    :param dictionary: dict
    :return: dynamic_object
    """
    obj = DynamicClass()
    for key in dictionary:
        setattr(obj, key, dictionary[key])
    return obj


def object_to_dict(object):
    """
    parse an object and return a dictionary
    :param object: object
    :return: dict
    """
    dictionary = {}
    obj_dict = object.__dict__
    for key in obj_dict:
        if not key.startswith('__'):
            dictionary[key] = obj_dict[key]
    return dictionary


def pop_by_name(items, name):
    """pop list item by its value"""
    if name in items:
        items.pop(name)
    return name


def swap(items, a, b):
    """swap between list/dict items values"""
    items[a], items[b] = items[b], items[a]
    return items


def dynamic_delay(t, max_delay):
    """ sleep dynamically by measuring the time passed
    since t started and sleeping the
    remaining of the delay

    :param t: time.time()
    :param max_delay: in seconds
    """
    t = time.time() - t
    if t < max_delay:
        time.sleep(max_delay - t)


def list_diff(list1, list2):
    """get the outer-section between lists
    example:
        a = ['a','b','c']
        b = ['a','b']
        list_diff(a, b)
        >['c']
    """
    s = set(list2)
    return [x for x in list1 if x not in s]


def string_to_ascii(string: str):
    """return string of ascii characters with _ as seperator"""
    return '_'.join(str(ord(c)) for c in string)


def ascii_to_string(string: str):
    """return ascii characters with _ as seperator to string"""
    return ''.join(chr(int(i)) for i in string.split('_'))
