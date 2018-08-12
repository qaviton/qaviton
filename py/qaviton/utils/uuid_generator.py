import uuid
import time
import datetime


class UniqueID:
    """ generate a uuid """

    @staticmethod
    def generate():
        return uuid.uuid4()

    @staticmethod
    def generate_timestamp():
        """ generate a millisecond timestamp uuid """
        then = datetime.datetime.now()
        return int(time.mktime(then.timestamp()) * 1e3 + then.microsecond / 1e3)
