import random
from faker import Faker


"""use this to create random names
print(fake.name())
> Rachel Cruz
"""
fake = Faker()


def random_number(minimum, maximum):
    """ get a random number from range
    :type minimum: int
    :type maximum: int
    :rtype: int
    """
    if minimum > maximum:
        maximum = minimum + 1
    numbers = []
    for number in range(minimum, maximum + 1):
        numbers.append(number)
    return random.SystemRandom().choice(numbers)


def no_space_egdes(string, s):
    if s.endswith(' '):
        string = string.replace(" ", "")
        if len(string) == 0:
            raise ValueError("random string cannot end with ' ' space.")

        if s.startswith(' '):
            s = random.SystemRandom().choice(string) + s[1:-1] + random.SystemRandom().choice(string)
        else:
            s = s[:-1] + random.SystemRandom().choice(string)

    elif s.startswith(' '):
        string = string.replace(" ", "")
        if len(string) == 0:
            raise ValueError("random string cannot start with ' ' space.")

        if s.endswith(' '):
            s = random.SystemRandom().choice(string) + s[1:-1] + random.SystemRandom().choice(string)
        else:
            s = random.SystemRandom().choice(string) + s[1:]
    return s


def random_string(string, length=1):
    """ get a random string from a string
    string cannot start/end with ' '
    :type length: int
    :type string: str
    :rtype: str
    """
    return no_space_egdes(string, ''.join(random.SystemRandom().choice(string) for _ in range(length)))


class strings:
    """
    class for different kind of strings
    """
    big_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    small_letters = "abcdefghijklmnopqrstuvwxyz"
    numbers = "0123456789"
    space = " "
    invalid_characters = "!@#$%^&*()-_=+`~/?.><\\][}{|"
    special_invalid_characters = "\"'"

    letters = big_letters + small_letters
    letters_and_numbers = letters + numbers
    characters = letters_and_numbers + space
    characters_with_invalid = characters + invalid_characters
    all_characters = characters_with_invalid + special_invalid_characters


class create_random:
    """get a random string
        WARNING: string cannot start/end with ' '(space)
    """
    @staticmethod
    def string(string=strings.characters_with_invalid, length=15):
        """ create random string from a given string.
        if no string is given then random string is created from:
        ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !@#$%^&*()-_=+`~/?.><\\][}{|

        :param string: string to create from
        :param length: generated random string length
        :rtype: str
        """
        return random_string(string, length)

    @staticmethod
    def all_characters(length=15):
        """ create random string from:
        ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !@#$%^&*()-_=+`~/?.><\\][}{|"'
        :param length: generated random string length
        :rtype: str
        """
        return random_string(strings.all_characters, length)

    @staticmethod
    def characters_with_invalid(length=15):
        """ create random string from:
        ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !@#$%^&*()-_=+`~/?.><\\][}{|
        :param length: generated random string length
        :rtype: str
        """
        return random_string(strings.characters_with_invalid, length)

    @staticmethod
    def characters(length=15):
        """ create random string from:
        ABCDEFGHIJKLMNOPQRSTUVWXYZ abcdefghijklmnopqrstuvwxyz0123456789
        :param length: generated random string length
        :rtype: str
        """
        return random_string(strings.characters, length)

    @staticmethod
    def letters_and_numbers(length=15):
        """ create random string from:
        ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
        :param length: generated random string length
        :rtype: str
        """
        return random_string(strings.letters_and_numbers, length)

    @staticmethod
    def letters(length=15):
        """ create random string from:
        ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
        :param length: generated random string length
        :rtype: str
        """
        return random_string(strings.letters, length)

    @staticmethod
    def invalid_characters(length=15):
        """ create random string from:
        !@#$%^&*()-_=+`~/?.><\\][}{|
        :param length: generated random string length
        :rtype: str
        """
        return random_string(strings.invalid_characters, length)

    @staticmethod
    def numbers(length=15):
        """ create random string from:
        0123456789
        :param length: generated random string length
        :rtype: str
        """
        return random_string(strings.numbers, length)

    @staticmethod
    def small_letters(length=15):
        """ create random string from:
        abcdefghijklmnopqrstuvwxyz
        :param length: generated random string length
        :rtype: str
        """
        return random_string(strings.small_letters, length)

    @staticmethod
    def big_letters(length=15):
        """ create random string from:
        ABCDEFGHIJKLMNOPQRSTUVWXYZ
        :param length: generated random string length
        :rtype: str
        """
        return random_string(strings.big_letters, length)

    @staticmethod
    def name(length=20):
        """ create random name from fake library:
        :param length: generated random string length
        :rtype: str
        """
        return fake.name()[:length]

    @staticmethod
    def number(minimum=1, maximum=10):
        """ create random number
        :type minimum: int
        :type maximum: int
        :rtype: int
        """
        return random_number(minimum, maximum)

    @staticmethod
    def from_items(items: list, number_of_choices=1):
        """select random items from list
        :param length: generated random string length
        :rtype: []
        """
        items = list(items)
        choices = []
        for i in range(number_of_choices):
            choice = random.SystemRandom().choice(items)
            choices.append(choice)
            items.remove(choice)
        return choices
