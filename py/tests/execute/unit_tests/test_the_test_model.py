import pytest
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from qaviton.crosstest import WebDriver
from qaviton.crosstest import MobileDriver
from qaviton import crosstest
from tests.settings import platforms
from tests.settings import TESTS
from tests.data.count_functions import from_zero_to_hero


@pytest.mark.parametrize('platform', platforms.get(), ids=crosstest.id)
def test_platforms(platform):
    if platform["testing_type"] == crosstest.TestAPI.WEB:
        assert platform["desired_capabilities"] == DesiredCapabilities.CHROME or \
               platform["desired_capabilities"] == DesiredCapabilities.FIREFOX
    elif platform["testing_type"] == crosstest.TestAPI.MOBILE:
        assert platform["desired_capabilities"] == platforms.mobile.get()[0]["desired_capabilities"]
    else:
        raise Exception("bad testing type value: {}".format(platform["testing_type"]))


@pytest.mark.parametrize('test', TESTS, ids=crosstest.id)
def test_models(test: crosstest.Model):
    if test.desired_capabilities in platforms.web or test.desired_capabilities == DesiredCapabilities.FIREFOX:
        assert test.test_api == crosstest.TestAPI.WEB
        assert test.command_executor == crosstest.WebPlatform.driver_url
        assert test.driver_api == WebDriver

    elif test.desired_capabilities == platforms.mobile.get()[0]["desired_capabilities"]:
        assert test.test_api == crosstest.TestAPI.MOBILE
        assert test.command_executor == crosstest.MobilePlatform.driver_url
        assert test.driver_api == MobileDriver

    else:
        raise Exception("desired capabilities not as expected: {}".format(test.desired_capabilities))

    assert test.data == from_zero_to_hero

