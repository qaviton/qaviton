import uuid
import time
import datetime


def generate():
    """ generate a uuid """
    return str(uuid.uuid4())


def generate_timestamp():
    """ generate a millisecond timestamp uuid """
    t = datetime.datetime.now()
    return int(time.mktime(t.timestamp()) * 1e3 + t.microsecond / 1e3)


"""
generate test id for parameterized tests
    example:
        from qaviton.utils.uuid_generator import uid
        import pytest
        
        @pytest.mark.parametrize('data', [from_zero_to_hero, from_zero_to_hero], ids=uid)  # get test data layer x2
        def test_platforms_and_data(platform: crosstest.Platform, data, request):
            test = platform.setup(request)
"""
id = lambda i: str(i.id)

print(generate())