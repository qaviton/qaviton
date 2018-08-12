# test runner
import pytest

# things for the tests
from tests.settings import platforms
from tests.data.count_functions import from_zero_to_hero

# things to test
from qaviton.crosstest import WebDriver
from qaviton.crosstest import MobileDriver
from qaviton import crosstest
from qaviton import settings
from qaviton.utils.uuid_generator import testid


@pytest.mark.parametrize('platform', platforms.get(), ids=testid)  # test per platform
def test_platforms(platform):

    if platform.platform["api"] == crosstest.API.WEB:
        assert platform.platform["desired_capabilities"]["browserName"] in ("firefox", "chrome", "internet explorer")
    elif platform.platform["api"] == crosstest.API.MOBILE:
        assert platform.platform["desired_capabilities"]['platformName'] in ("Android",)
    else:
        raise Exception("bad testing type value: {}".format(platform.platform["api"]))


@pytest.mark.parametrize('platform', platforms.get(), ids=testid)  # get test platform layer x4
@pytest.mark.parametrize('data', [from_zero_to_hero, from_zero_to_hero], ids=testid)  # get test data layer x2
def test_platforms_and_data(platform: crosstest.Platform, data, request):
    test = platform.setup(request)

    if test.platform["api"] == WebDriver:
        assert test.platform["command_executor"] == settings.webdriver_url
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


####################################
# you can ignore these tests below #
####################################


@pytest.mark.skip(reason="just testing double parameters for cross-platform & data-driven testing (it's a one shot)")
@pytest.mark.parametrize('test', [0.0,1.0,2.0], ids=testid)
@pytest.mark.parametrize('data', [0,1,2,3], ids=testid)
def test_2_layered_data(test, data):
    print(test, data)


@pytest.mark.skip(reason="don't run this its a script")
def test_all_drivers_are_done():
    import psutil

    for proc in psutil.process_iter():
        try:
            if "chrome" in proc.name():
                p = psutil.Process(proc.pid)
                # if 'SYSTEM' not in p.username:
                proc.kill()
        except Exception as e:
            print(e)
