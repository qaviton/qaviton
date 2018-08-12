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


"""
generate test id for parameterized tests
    example:
        from qaviton.utils.uuid_generator import testid
        import pytest
        
        @pytest.mark.parametrize('data', [from_zero_to_hero, from_zero_to_hero], ids=testid)  # get test data layer x2
        def test_platforms_and_data(platform: crosstest.Platform, data, request):
            test = platform.setup(request)
"""
testid = lambda i: str(i.id)
