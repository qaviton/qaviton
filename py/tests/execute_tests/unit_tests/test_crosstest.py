# test runner
import pytest

# things for the tests
from tests.config.supported_platforms import platforms
from tests.config.count_functions import from_zero_to_hero

# things to test
from qaviton.crosstest import WebDriver
from qaviton.crosstest import MobileDriver
from qaviton import crosstest
from qaviton import settings
from qaviton.utils import unique_id


@pytest.mark.parametrize('platform', platforms.get(), ids=unique_id.id)  # test per platform
def test_platforms(platform):
    if platform.platform["api"] == crosstest.API.WEB:
        assert platform.platform["desired_capabilities"]["browserName"] in ("firefox", "chrome", "internet explorer")
    elif platform.platform["api"] == crosstest.API.MOBILE:
        assert platform.platform["desired_capabilities"]['platformName'] in ("Android",)
    else:
        raise Exception("bad testing type value: {}".format(platform.platform["api"]))


@pytest.mark.parametrize('platform', platforms.get(), ids=unique_id.id)  # get test platform layer x4
@pytest.mark.parametrize('data', [from_zero_to_hero, from_zero_to_hero], ids=unique_id.id)  # get test data layer x2
def test_platforms_and_data(platform: crosstest.Platform, data, request):
    test = platform.setup(request)

    if test.platform["api"] == WebDriver:
        assert test.platform["command_executor"] == platforms.web.command_executor
        assert test.platform["desired_capabilities"]["browserName"] in ("firefox", "chrome", "internet explorer")

    elif test.platform["api"] == MobileDriver:
        assert test.platform["command_executor"] == settings.mobiledriver_url
        assert test.platform["desired_capabilities"]['platformName'] in ("Android",)

    else:
        raise Exception("test case object not as expected: {}".format(vars(test)))

    assert data == from_zero_to_hero


# health check
@pytest.mark.critical
def test_all_threads_are_done():
    import threading
    assert threading.active_count() == 1

